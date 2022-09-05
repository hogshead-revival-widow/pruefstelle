<script lang="ts">
	import { createForm, Form, Field, ErrorMessage } from 'svelte-forms-lib';

	import Card from '$lib/components/basic/Card.svelte';
	import { getMailSchema } from '$lib/data/schemas';
	import { updateEmail } from '$lib/scripts/user';
	import { user } from '$lib/stores';

	const formProps = {
		initialValues: {
			password: '',
			email: '',
			emailConfirm: ''
		},
		validationSchema: getMailSchema($user.email),
		onSubmit: (values) => updateEmail(values)
	};

	const formContext = createForm(formProps);
	const { errors } = formContext;
</script>

<Card isHideable={false} classes={['max-w-md', 'w-96', 'h-fit']}>
	<svelte:fragment slot="title">Meine Email-Adresse ändern</svelte:fragment>

	<article>
		<Form id="changeEmail" context={formContext} class="form-control" novalidate>
			<label class="label" for="username">
				<span class="label-text text-primary-content">Email</span>
				<ErrorMessage class="label-text text-error contrast-200" name="email" />
			</label>

			<Field
				id="email"
				type="email"
				class="input  {$errors.email ? 'input-error' : 'input-primary'} text-base-content"
				placeholder="Email eingeben"
				name="email"
				autocomplete="email" />

			<label class="label" for="password">
				<span class="label-text text-primary-content">Email bestätigen</span>
				<ErrorMessage class="label-text text-error contrast-200" name="emailConfirm" />
			</label>
			<Field
				id="current-password"
				type="email"
				name="emailConfirm"
				class="input {$errors.emailConfirm ? 'input-error' : 'input-primary'} text-base-content"
				placeholder="Email bestätigen"
				autocomplete="email" />

			<label class="label" for="username">
				<span class="label-text text-primary-content">Aktuelles Passwort</span>
				<ErrorMessage class="label-text text-error contrast-200" name="password" />
			</label>

			<Field
				id="password"
				type="password"
				class="input  {$errors.password ? 'input-error' : 'input-primary'} text-base-content"
				placeholder="Aktuelles Passwort"
				name="password"
				autocomplete="current-password" />

			<button class="mt-6 btn btn-primary" type="submit">Ändern</button>
		</Form>
	</article>
</Card>
