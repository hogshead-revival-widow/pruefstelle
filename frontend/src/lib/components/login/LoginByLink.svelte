<script lang="ts">
	/*
		Let a user login by link
	*/
	import { fade } from 'svelte/transition';
	import { createForm, Form, Field, ErrorMessage } from 'svelte-forms-lib';
	import { Pruefstelle } from '$lib/api';
	import { loginByLinkSchema } from '$lib/data/schemas';
	export let email = '';
	export let isDisabled: boolean;

	let mailSent = false;

	const sendLoginLink = async (email: string) => {
		try {
			await Pruefstelle.sendLoginLink({ email });
			mailSent = true;
		} catch (error) {
			if (error.status === 400 || error.status === 401 || error.status === 404) {
				$errors.email = 'Email/Passwort falsch';
			} else {
				isDisabled = true;
			}
		}
	};
	const formProps = {
		initialValues: {
			email: email
		},
		validationSchema: loginByLinkSchema,
		onSubmit: async (values) => {
			const { email } = values;
			await sendLoginLink(email);
		}
	};

	const formContext = createForm(formProps);
	const { errors, form } = formContext;

	$: email = $form.email;
</script>

<article>
	{#if mailSent}
		<div in:fade class="mt-4 mb-4 ">
			<p class="mb-2">Anmelde-Link verschickt!</p>
			<p>
				Klicke innerhalb der nächsten zehn Minuten auf den Link in deinem Email-Postfach, um dich
				einzuloggen.
			</p>
		</div>
	{:else}
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

			<button class="mt-6 btn btn-ghost" type="submit">Ohne Passwort anmelden</button>
		</Form>
	{/if}
</article>
