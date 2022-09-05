<script lang="ts">
	import Card from '$lib/components/basic/Card.svelte';
	import { createForm, Form, Field, ErrorMessage } from 'svelte-forms-lib';
	import { passwordSchema } from '$lib/data/schemas';
	import { updatePassword } from '$lib/scripts/user';

	const formProps = {
		initialValues: {
			currentPassword: '',
			password: '',
			passwordConfirm: ''
		},
		validationSchema: passwordSchema,
		onSubmit: (values) => updatePassword(values)
	};

	const formContext = createForm(formProps);
	const { errors } = formContext;
</script>

<Card isHideable={false} classes={['max-w-md', 'w-96', 'h-fit']}>
	<svelte:fragment slot="title">Mein Passwort ändern</svelte:fragment>

	<article>
		<Form id="changePassword" context={formContext} class="form-control" novalidate>
			<label class="label" for="password">
				<span class="label-text text-primary-content">Neues Passwort</span>
				<ErrorMessage class="label-text text-error contrast-200" name="password" />
			</label>
			<Field
				id="password"
				type="password"
				name="password"
				class="input {$errors.password ? 'input-error' : 'input-primary'} text-base-content"
				placeholder="Neues Passwort"
				autocomplete="new-password" />

			<label class="label" for="passwordConfirm">
				<span class="label-text text-primary-content">Neues Passwort bestätigen</span>
				<ErrorMessage class="label-text text-error contrast-200" name="passwordConfirm" />
			</label>
			<Field
				id="passwordConfirm"
				type="password"
				name="passwordConfirm"
				class="input {$errors.passwordConfirm ? 'input-error' : 'input-primary'} text-base-content"
				placeholder="Neues Passwort bestätigen"
				autocomplete="new-password" />

			<label class="label" for="username">
				<span class="label-text text-primary-content">Altes Passwort</span>
				<ErrorMessage class="label-text text-error contrast-200" name="currentPassword" />
			</label>

			<Field
				id="currentPassword"
				type="password"
				class="input  {$errors.currentPassword ? 'input-error' : 'input-primary'} text-base-content"
				placeholder="Bisheriges Passwort"
				name="currentPassword"
				autocomplete="password" />

			<button class="mt-6 btn btn-primary" type="submit">Ändern</button>
		</Form>
	</article>
</Card>
