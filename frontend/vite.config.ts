import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, '.', '');
	const apiTarget = env.VITE_API_PROXY_TARGET || 'http://127.0.0.1:8000';

	return {
		plugins: [sveltekit()],
		server: {
			proxy: {
				'/api': {
					target: apiTarget,
					changeOrigin: true
				},
				'/admin': {
					target: apiTarget,
					changeOrigin: true
				}
			}
		},
		preview: {
			proxy: {
				'/api': {
					target: apiTarget,
					changeOrigin: true
				},
				'/admin': {
					target: apiTarget,
					changeOrigin: true
				}
			}
		}
	};
});
