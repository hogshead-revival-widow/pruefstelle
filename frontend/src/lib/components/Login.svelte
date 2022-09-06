<script lang="ts">
	/*
		Let a user login
	*/
	import { goto } from '$app/navigation';
	import { createForm, Form, Field, ErrorMessage } from 'svelte-forms-lib';

	import { loginSchema } from '$lib/data/schemas';
	import { handleLogin } from '$lib/scripts/auth';

	export let redirect = '/dashboard';
	export let email = '';
	export let isDisabled: boolean;

	const on401Error = () => {
		$errors.email = 'Email/Passwort falsch';
		$errors.password = 'Email/Passwort falsch';
	};

	const onOtherError = () => {
		isDisabled = true;
	};

	const onLoggedIn = () => {
		goto(redirect);
	};

	const formProps = {
		initialValues: {
			email: email,
			password: ''
		},
		validationSchema: loginSchema,
		onSubmit: (values) => {
			const handlers = { on401Error, onOtherError, onLoggedIn };
			handleLogin(values, handlers);
		}
	};

	const formContext = createForm(formProps);
	const { errors, form } = formContext;

	$: email = $form.email;
</script>

<article>
	<Form
		id="authLogin"
		context={formContext}
		action="/auth/api/auth"
		method="post"
		class="form-control"
		novalidate>
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
			<span class="label-text text-primary-content">Passwort</span>
			<ErrorMessage class="label-text text-error contrast-200" name="password" />
		</label>
		<Field
			id="current-password"
			type="password"
			name="password"
			class="input {$errors.password ? 'input-error' : 'input-primary'} text-base-content"
			placeholder="Passwort eingeben"
			autocomplete="current-password" />

		<button class="mt-6 btn btn-ghost" type="submit">Anmelden</button>
	</Form>
</article>
