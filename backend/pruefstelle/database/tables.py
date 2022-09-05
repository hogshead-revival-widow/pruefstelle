import enum
import uuid


from sqlalchemy import Column, ForeignKey, String, Boolean, Integer, Table, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .config import mapper_registry
from .mixins import WithTablename, WithID, WithIDTitleDateCreator, WithDate, WithCreator

"""
Link Tables
"""


CaseDocumentLink = Table(
    "case_document_link",
    mapper_registry.metadata,
    Column("case_id", ForeignKey("case.id"), primary_key=True),
    Column("document_id", ForeignKey("document.id"), primary_key=True),
)

UserCaseLink = Table(
    "user_case_link",
    mapper_registry.metadata,
    Column("case_id", ForeignKey("case.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)


ItemItemLink = Table(
    "item_item_link",
    mapper_registry.metadata,
    Column("parent_item_id", ForeignKey("item.id"), primary_key=True),
    Column("child_item_id", ForeignKey("item.id"), primary_key=True),
)


MiningJobMiningResultLink = Table(
    "mining_job_mining_result_link",
    mapper_registry.metadata,
    Column("mining_job_id", ForeignKey("mining_job.id"), primary_key=True),
    Column("mining_result_id", ForeignKey("mining_result.id"), primary_key=True),
)

"""
User
"""


@mapper_registry.mapped
class User(WithTablename, WithID):

    email = Column(String(320), nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    superuser = Column(Boolean, nullable=False, default=False)
    watching = relationship("Case", secondary=UserCaseLink, back_populates="watchers")


"""
Case
"""


@mapper_registry.mapped
class Case(WithTablename, WithIDTitleDateCreator):
    frozen = Column(Boolean, nullable=False, default=False)

    original_case_id = Column(ForeignKey("case.id"), default=None)
    original_case = relationship("Case", uselist=False)

    category_id = Column(ForeignKey("category.id"), nullable=False)
    category = relationship("CaseCategory", uselist=False, lazy="selectin")

    watchers = relationship("User", secondary=UserCaseLink, back_populates="watching")

    documents = relationship(
        "Document", secondary=CaseDocumentLink, back_populates="cases"
    )

    profile_id = Column(ForeignKey("profile.id"), nullable=False)
    profile = relationship(
        "Profile", uselist=False, lazy="selectin", cascade="all,delete"
    )

    watchers_link_model = UserCaseLink
    document_link_model = CaseDocumentLink


"""
Document
"""


@mapper_registry.mapped
class Document(WithTablename, WithIDTitleDateCreator):

    category_id = Column(ForeignKey("category.id"), nullable=False)
    category = relationship(
        "DocumentCategory",
        lazy="selectin",
        uselist=False,
        foreign_keys=[category_id],
    )

    external_id = Column(String, default=None)

    external_id_category_id = Column(ForeignKey("category.id"))
    external_id_category = relationship(
        "ExternalIDCategory",
        foreign_keys=[external_id_category_id],
        lazy="selectin",
        uselist=False,
    )

    cases = relationship("Case", secondary=CaseDocumentLink, back_populates="documents")

    case_link_model = CaseDocumentLink

    items = relationship(
        "Item", back_populates="document", cascade="all,delete, delete-orphan"
    )


"""
Category, and  inherting from Category (Single Table Inheritance)
"""


class CategoryType(str, enum.Enum):
    CaseCategory = "case_category"
    DocumentCategory = "document_category"
    SourceCategory = "source_category"
    ExternalIDCategory = "external_id_category"
    TextCategory = "text_category"

    def get_model(self):
        return globals()[self.name]


@mapper_registry.mapped
class Category(WithTablename, WithID):

    name = Column(String(255), nullable=False)
    discriminator = Column(String(50), nullable=False)
    ndb_norm_id = Column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_on": "discriminator",
        "polymorphic_identity": "category",
    }


@mapper_registry.mapped
class CaseCategory(Category):
    __mapper_args__ = {"polymorphic_identity": CategoryType.CaseCategory}


@mapper_registry.mapped
class DocumentCategory(Category):
    __mapper_args__ = {"polymorphic_identity": CategoryType.DocumentCategory}


@mapper_registry.mapped
class SourceCategory(Category):
    __mapper_args__ = {"polymorphic_identity": CategoryType.SourceCategory}


@mapper_registry.mapped
class ExternalIDCategory(Category):

    source_id = Column(ForeignKey("category.id"))

    source = relationship(
        "SourceCategory",
        uselist=False,
        remote_side=[Category.id],
        lazy="selectin",
        join_depth=2,
    )

    __mapper_args__ = {"polymorphic_identity": CategoryType.ExternalIDCategory}


@mapper_registry.mapped
class TextCategory(Category):
    __mapper_args__ = {"polymorphic_identity": CategoryType.TextCategory}


"""
Item, and  inherting from Item (Joined Table Inheritance)
Note:
    - don't use the WithTableName mixin here, instead declare the name explicitly
"""


class ItemType(str, enum.Enum):
    Text = "text"

    def get_model(self):
        return globals()[self.name]


@mapper_registry.mapped
class Item(WithDate, WithCreator):
    __tablename__ = "item"

    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
    )

    discriminator = Column(String(50), nullable=False)

    document_id = Column(ForeignKey("document.id"), nullable=False)
    document = relationship("Document", foreign_keys=[document_id])

    source_category_id = Column(ForeignKey("category.id"), nullable=False)
    source_category = relationship(
        "SourceCategory",
        foreign_keys=[source_category_id],
        uselist=False,
        lazy="selectin",
    )

    parents = relationship(
        "Item",
        secondary=ItemItemLink,
        primaryjoin=id == ItemItemLink.c.child_item_id,
        secondaryjoin=id == ItemItemLink.c.parent_item_id,
    )

    research_quality_snapshots = relationship(
        "ResearchQualitySnapshot", back_populates="item"
    )
    mining_jobs = relationship(
        "MiningJob",
        back_populates="item",
        cascade="all,delete,delete-orphan",
    )
    mining_results = relationship(
        "MiningResult", back_populates="item", lazy="selectin"
    )

    item_link_model = ItemItemLink

    __mapper_args__ = {
        "polymorphic_on": "discriminator",
        "polymorphic_identity": "item",
    }


@mapper_registry.mapped
class Text(Item):
    __tablename__ = "text"

    item_id = Column(ForeignKey("item.id"), primary_key=True)

    content = Column(String, nullable=False)

    category_id = Column(ForeignKey("category.id"))
    category = relationship(
        "TextCategory",
        foreign_keys=[category_id],
        uselist=False,
        lazy="selectin",
    )

    @property
    def title(self, limit=15):
        content = str(self.content)
        return content[:limit] + "..." * int((len(content) > limit))

    __mapper_args__ = {"polymorphic_identity": ItemType.Text}


"""
Research Quality Snapshot
"""


@mapper_registry.mapped
class ResearchQualitySnapshot(WithTablename, WithID, WithDate):
    points = Column(DECIMAL(3, 2), nullable=False)
    item_id = Column(ForeignKey("item.id"), nullable=False)
    item = relationship("Item", back_populates="research_quality_snapshots")
    profile_id = Column(ForeignKey("profile.id"), nullable=False)
    profile = relationship("Profile", back_populates="research_quality_snapshots")


"""
Mining-related Tables
"""


@mapper_registry.mapped
class MiningJob(WithTablename, WithID, WithDate, WithCreator):
    status = Column(String(50), nullable=False)
    service = Column(String(50), nullable=False)

    # Refers to an id provided by the service
    # Don't confuse it with 'external_id' in Document
    external_id = Column(String)

    item_id = Column(ForeignKey("item.id"), nullable=False)
    item = relationship("Item", back_populates="mining_jobs", lazy="selectin")

    results = relationship(
        "MiningResult", secondary=MiningJobMiningResultLink, back_populates="jobs"
    )


class ResultType(str, enum.Enum):
    Keyword = "result_keyword"
    NamedEntity = "result_named_entity"

    def get_model(self):
        return globals()[self.name]


@mapper_registry.mapped
class MiningResult(WithDate):
    __tablename__ = "mining_result"
    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
    )

    item_id = Column(ForeignKey("item.id"), nullable=False)
    item = relationship("Item", back_populates="mining_results")

    discriminator = Column(String(50), nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    evaluations = relationship(
        "Evaluation", back_populates="mining_result", lazy="selectin"
    )
    jobs = relationship(
        "MiningJob", secondary=MiningJobMiningResultLink, back_populates="results"
    )

    mining_job_mining_result_link_model = MiningJobMiningResultLink

    __mapper_args__ = {
        "polymorphic_on": "discriminator",
        "polymorphic_identity": "mining_result",
        "with_polymorphic": "*",
    }


@mapper_registry.mapped
class Keyword(MiningResult):
    __tablename__ = "keyword"

    mining_result_id = Column(ForeignKey("mining_result.id"), primary_key=True)

    keyword = Column(String(255), nullable=False)
    relevance = Column(DECIMAL(10, 2), nullable=False)
    frequency = Column(Integer, nullable=False)
    confidence = Column(DECIMAL(10, 2), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": ResultType.Keyword,
        "polymorphic_load": "inline",
    }


@mapper_registry.mapped
class NamedEntity(MiningResult):
    __tablename__ = "named_entity"

    mining_result_id = Column(ForeignKey("mining_result.id"), primary_key=True)

    type = Column(String(50), nullable=False)
    label = Column(String(255), nullable=False)
    begin = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": ResultType.NamedEntity,
        "polymorphic_load": "inline",
    }


"""
Profile
"""


@mapper_registry.mapped
class Profile(WithTablename, WithID):
    """
    Every profile attribute condition that has one of the following prefixes:
    - keyword_ -> applied BEFORE calculation of points has been started, cf. tasks.points.options
    - research_quality_constraint -> applied AFTER calculation of points has been started, , cf.tasks.points.constraints
    """

    keyword_relevance_threshold = Column(Integer, nullable=False)
    keyword_confidence_threshold = Column(Integer, nullable=False)
    keyword_frequency_threshold = Column(Integer, nullable=False)
    keyword_only_top_n_relevance = Column(Integer, nullable=False)
    research_quality_constraint_needed_users = Column(Integer, nullable=False)
    research_quality_good_threshold = Column(Integer, nullable=False, default=50)

    research_quality_snapshots = relationship(
        "ResearchQualitySnapshot", back_populates="profile"
    )


"""
Evaluation
"""


class EvaluationType(str, enum.Enum):
    ScoredEvaluation = "scored_evaluation"
    CorrectnessEvaluation = "correctness_evaluation"

    def get_model(self):
        return globals()[self.name]


@mapper_registry.mapped
class Evaluation(WithTablename, WithID, WithDate, WithCreator):

    value = Column(Integer, nullable=False)

    mining_result_id = Column(ForeignKey("mining_result.id"))  # nullable=False
    mining_result = relationship("MiningResult", back_populates="evaluations")

    discriminator = Column(String(50), nullable=False)
    discriminatorType = EvaluationType

    __mapper_args__ = {
        "polymorphic_on": "discriminator",
        "polymorphic_identity": "evaluation",
    }


@mapper_registry.mapped
class ScoredEvaluation(Evaluation):
    __mapper_args__ = {"polymorphic_identity": EvaluationType.ScoredEvaluation}


@mapper_registry.mapped
class CorrectnessEvaluation(Evaluation):
    __mapper_args__ = {"polymorphic_identity": EvaluationType.CorrectnessEvaluation}


"""
Magic Link
"""


@mapper_registry.mapped
class MagicLink(WithTablename, WithDate):
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    value = Column(String(255), nullable=False)
    user = relationship("User")
