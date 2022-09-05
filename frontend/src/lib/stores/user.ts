import { writable, type Writable } from 'svelte/store';
import type { ps } from '$lib/api';

export const DefaultUser = () => Object.create({ id: undefined, email: undefined });
export const user: Writable<ps.UserRead> = writable(DefaultUser());
