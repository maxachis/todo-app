<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import { api, type GraphData } from '$lib';

	let graphEl: HTMLDivElement | null = $state(null);
	let detailsEl: HTMLDivElement | null = $state(null);
	let searchInput: HTMLInputElement | null = $state(null);
	let searchResultsEl: HTMLDivElement | null = $state(null);
	let spacingInput: HTMLInputElement | null = $state(null);
	let repulsionInput: HTMLInputElement | null = $state(null);
	let centeringInput: HTMLInputElement | null = $state(null);
	let hideIsolatedInput: HTMLInputElement | null = $state(null);
	let showEdgeNotesInput: HTMLInputElement | null = $state(null);
	let labelSizeInput: HTMLInputElement | null = $state(null);

	let filterPeople: HTMLInputElement | null = $state(null);
	let filterOrganizations: HTMLInputElement | null = $state(null);
	let filterPersonPerson: HTMLInputElement | null = $state(null);
	let filterOrgPerson: HTMLInputElement | null = $state(null);

	onMount(async () => {
		if (!graphEl || !detailsEl) return;
		const raw = await api.graph.get();

		const renderDetails = (data: any | null) => {
			if (!detailsEl) return;
			if (!data) {
				detailsEl.innerHTML = '<p>Hover over a node to see details.</p>';
				return;
			}
			const title = data.details?.name || data.label || 'Details';
			const type = data.type || 'node';
			const notes = data.details?.notes || '';
			const orgType = data.details?.type || '';
			detailsEl.innerHTML = `
        <div class="space-y-2">
          <div class="text-base font-semibold">${title}</div>
          <div class="text-xs uppercase tracking-wide text-gray-500">${type}</div>
          ${orgType ? `<div class="text-sm"><span class="font-medium">Type:</span> ${orgType}</div>` : ''}
          ${notes ? `<div class="text-sm"><span class="font-medium">Notes:</span> ${notes}</div>` : ''}
        </div>
      `;
		};

		const renderEdgeDetails = (data: any | null) => {
			if (!detailsEl) return;
			if (!data) {
				renderDetails(null);
				return;
			}
			const type = data.type || 'edge';
			const notes = data.notes || '';
			detailsEl.innerHTML = `
        <div class="space-y-2">
          <div class="text-base font-semibold">Relationship</div>
          <div class="text-xs uppercase tracking-wide text-gray-500">${type}</div>
          ${notes ? `<div class="text-sm"><span class="font-medium">Notes:</span> ${notes}</div>` : ''}
        </div>
      `;
		};

		const applyFilters = (nodes: any[], links: any[]) => {
			const enabled = new Set<string>();
			if (filterPeople?.checked) enabled.add('person');
			if (filterOrganizations?.checked) enabled.add('organization');
			if (filterPersonPerson?.checked) enabled.add('person-person');
			if (filterOrgPerson?.checked) enabled.add('organization-person');

			nodes.forEach((node) => {
				node.hidden = !enabled.has(node.type);
			});

			const visibleNodeIds = new Set(nodes.filter((node) => !node.hidden).map((node) => node.id));
			links.forEach((link) => {
				link.hidden =
					!enabled.has(link.type) ||
					!visibleNodeIds.has(link.source.id || link.source) ||
					!visibleNodeIds.has(link.target.id || link.target);
			});

			if (hideIsolatedInput?.checked) {
				const connectedNodeIds = new Set<string>();
				links.forEach((link) => {
					if (!link.hidden) {
						connectedNodeIds.add(link.source.id || link.source);
						connectedNodeIds.add(link.target.id || link.target);
					}
				});

				nodes.forEach((node) => {
					if (!node.hidden && !connectedNodeIds.has(node.id)) {
						node.hidden = true;
					}
				});
			}
		};

		const initGraph = (data: GraphData) => {
			if (!graphEl) return;
			const nodes = data.nodes.map((node) => ({
				id: node.data.id,
				label: node.data.label,
				type: node.data.type,
				details: node.data.details
			}));

			const links = data.edges.map((edge) => ({
				id: edge.data.id,
				source: edge.data.source,
				target: edge.data.target,
				type: edge.data.type,
				notes: edge.data.notes
			}));

			const width = graphEl.clientWidth;
			const height = graphEl.clientHeight;

			const svg = d3
				.select(graphEl)
				.append('svg')
				.attr('viewBox', [0, 0, width, height])
				.attr('class', 'w-full h-full');

			const zoomLayer = svg.append('g').attr('class', 'zoom-layer');
			const linkGroup = zoomLayer.append('g').attr('class', 'links');
			const linkLabelGroup = zoomLayer.append('g').attr('class', 'link-labels');
			const nodeGroup = zoomLayer.append('g').attr('class', 'nodes');
			const labelGroup = zoomLayer.append('g').attr('class', 'labels');

			const zoom = d3.zoom<SVGSVGElement, unknown>().scaleExtent([0.3, 3]).on('zoom', (event) => {
				zoomLayer.attr('transform', event.transform);
			});

			svg.call(zoom);

			const linkForce = d3.forceLink(links).id((d: any) => d.id).distance(140);
			const chargeForce = d3.forceManyBody().strength(-500);
			const collideForce = d3.forceCollide(18);
			const xForce = d3.forceX(width / 2).strength(0.06);
			const yForce = d3.forceY(height / 2).strength(0.06);

			const simulation = d3
				.forceSimulation(nodes as any)
				.force('link', linkForce)
				.force('charge', chargeForce)
				.force('center', d3.forceCenter(width / 2, height / 2))
				.force('x', xForce)
				.force('y', yForce)
				.force('collide', collideForce);

			const link = linkGroup
				.selectAll('line')
				.data(links, (d: any) => d.id)
				.join('line')
				.attr('stroke', '#9ca3af')
				.attr('stroke-width', 1.5)
				.on('mouseenter', (_event, d: any) => renderEdgeDetails(d))
				.on('mouseleave', () => renderDetails(null));

			const linkLabels = linkLabelGroup
				.selectAll('text')
				.data(links, (d: any) => d.id)
				.join('text')
				.text((d: any) => d.notes || '')
				.attr('font-size', 10)
				.attr('fill', '#6b7280')
				.attr('text-anchor', 'middle')
				.attr('dy', -4)
				.attr('display', 'none');

			const node = nodeGroup
				.selectAll('circle')
				.data(nodes, (d: any) => d.id)
				.join('circle')
				.attr('r', (d: any) => (d.type === 'organization' ? 9 : 7))
				.attr('fill', (d: any) => (d.type === 'organization' ? '#f97316' : '#4f46e5'))
				.call(
					d3
						.drag<any, any>()
						.on('start', (event, d: any) => {
							if (!event.active) simulation.alphaTarget(0.2).restart();
							d.fx = d.x;
							d.fy = d.y;
						})
						.on('drag', (event, d: any) => {
							d.fx = event.x;
							d.fy = event.y;
						})
						.on('end', (event, d: any) => {
							if (!event.active) simulation.alphaTarget(0);
							d.fx = null;
							d.fy = null;
						})
				)
				.on('mouseenter', (_event, d: any) => renderDetails(d))
				.on('mouseleave', () => renderDetails(null));

			const labels = labelGroup
				.selectAll('text')
				.data(nodes, (d: any) => d.id)
				.join('text')
				.text((d: any) => d.label)
				.attr('font-size', 11)
				.attr('fill', '#374151')
				.attr('text-anchor', 'middle')
				.attr('dy', -12);

			const refreshVisibility = () => {
				applyFilters(nodes, links);
				node.attr('display', (d: any) => (d.hidden ? 'none' : 'block'));
				labels.attr('display', (d: any) => (d.hidden ? 'none' : 'block'));
				link.attr('display', (d: any) => (d.hidden ? 'none' : 'block'));
				linkLabels.attr('display', (d: any) => {
					if (d.hidden) return 'none';
					return showEdgeNotesInput?.checked ? 'block' : 'none';
				});
			};

			const updateLabelSize = () => {
				const size = Number(labelSizeInput?.value ?? 11);
				labels.attr('font-size', size);
			};

			const updateForces = () => {
				const spacing = Number(spacingInput?.value ?? 140);
				const repulsion = Number(repulsionInput?.value ?? 500);
				const centering = Number(centeringInput?.value ?? 60);

				linkForce.distance(spacing);
				chargeForce.strength(-repulsion);
				xForce.strength(centering / 1000);
				yForce.strength(centering / 1000);
				simulation.alpha(0.5).restart();
			};

			const search = () => {
				const term = searchInput?.value.toLowerCase().trim() ?? '';
				if (!searchResultsEl) return;
				if (!term) {
					searchResultsEl.textContent = '';
					return;
				}
				const matches = nodes.filter((node) => node.label.toLowerCase().includes(term)).slice(0, 8);
				searchResultsEl.innerHTML = matches
					.map((node) => `<div class=\"result\" data-id=\"${node.id}\">${node.label}</div>`)
					.join('');
				Array.from(searchResultsEl.querySelectorAll<HTMLDivElement>('.result')).forEach((el) => {
					el.onclick = () => {
						const match = nodes.find((node) => node.id === el.dataset.id);
						if (match) {
							renderDetails(match);
							searchResultsEl.textContent = '';
							searchInput && (searchInput.value = '');
						}
					};
				});
			};

			const updatePositions = () => {
				node
					.attr('cx', (d: any) => d.x ?? 0)
					.attr('cy', (d: any) => d.y ?? 0);
				labels
					.attr('x', (d: any) => d.x ?? 0)
					.attr('y', (d: any) => d.y ?? 0);
				link
					.attr('x1', (d: any) => d.source.x ?? 0)
					.attr('y1', (d: any) => d.source.y ?? 0)
					.attr('x2', (d: any) => d.target.x ?? 0)
					.attr('y2', (d: any) => d.target.y ?? 0);
				linkLabels
					.attr('x', (d: any) => (d.source.x + d.target.x) / 2)
					.attr('y', (d: any) => (d.source.y + d.target.y) / 2);
			};

			simulation.on('tick', updatePositions);

			const attachInput = (el: HTMLInputElement | null) => {
				el?.addEventListener('input', () => {
					refreshVisibility();
					updateLabelSize();
					updateForces();
					search();
				});
				el?.addEventListener('change', () => {
					refreshVisibility();
					updateLabelSize();
					updateForces();
					search();
				});
			};

			attachInput(filterPeople);
			attachInput(filterOrganizations);
			attachInput(filterPersonPerson);
			attachInput(filterOrgPerson);
			attachInput(hideIsolatedInput);
			attachInput(showEdgeNotesInput);
			attachInput(spacingInput);
			attachInput(repulsionInput);
			attachInput(centeringInput);
			attachInput(labelSizeInput);

			searchInput?.addEventListener('input', search);

			refreshVisibility();
		};

		initGraph(raw);
	});
</script>

<section class="graph-page">
	<header>
		<h1>Graph</h1>
	</header>

	<div class="graph-grid">
		<div class="panel">
			<div class="card">
				<h2>Filters</h2>
				<div class="stack">
					<label><input type="checkbox" bind:this={filterPeople} checked /> People</label>
					<label><input type="checkbox" bind:this={filterOrganizations} checked /> Organizations</label>
					<label><input type="checkbox" bind:this={filterPersonPerson} checked /> Person ↔ Person</label>
					<label><input type="checkbox" bind:this={filterOrgPerson} checked /> Organization → Person</label>
					<label><input type="checkbox" bind:this={hideIsolatedInput} /> Hide isolated nodes</label>
					<label><input type="checkbox" bind:this={showEdgeNotesInput} /> Show relationship notes</label>
				</div>
			</div>

			<div class="card">
				<h2>Search</h2>
				<div class="stack">
					<input bind:this={searchInput} type="text" placeholder="Search people or organizations" />
					<div bind:this={searchResultsEl} class="search-results"></div>
				</div>
			</div>

			<div class="card">
				<h2>Layout</h2>
				<div class="stack">
					<label>
						<span>Spacing</span>
						<input bind:this={spacingInput} type="range" min="60" max="220" value="140" />
					</label>
					<label>
						<span>Repulsion</span>
						<input bind:this={repulsionInput} type="range" min="200" max="2000" value="500" />
					</label>
					<label>
						<span>Centering</span>
						<input bind:this={centeringInput} type="range" min="0" max="200" value="60" />
					</label>
					<label>
						<span>Label size</span>
						<input bind:this={labelSizeInput} type="range" min="8" max="18" value="11" />
					</label>
				</div>
			</div>

			<div class="card">
				<h2>Details</h2>
				<div bind:this={detailsEl} class="details"><p>Hover over a node to see details.</p></div>
			</div>
		</div>

		<div class="panel graph-panel">
			<div bind:this={graphEl} class="graph-canvas"></div>
		</div>
	</div>
</section>

<style>
	.graph-page {
		display: grid;
		gap: 1rem;
	}

	h1 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.5rem;
	}

	.graph-grid {
		display: grid;
		grid-template-columns: minmax(260px, 1fr) minmax(400px, 3fr);
		gap: 1rem;
	}

	.panel {
		display: grid;
		gap: 0.75rem;
	}

	.card {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 0.9rem;
		box-shadow: var(--shadow-sm);
		display: grid;
		gap: 0.6rem;
	}

	h2 {
		margin: 0;
		font-size: 1rem;
		font-family: var(--font-display);
	}

	.stack {
		display: grid;
		gap: 0.35rem;
		font-size: 0.85rem;
		color: var(--text-secondary);
	}

	label {
		display: grid;
		gap: 0.25rem;
	}

	input[type='text'],
	input[type='range'] {
		width: 100%;
	}

	input[type='text'] {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
	}

	.details {
		font-size: 0.85rem;
		color: var(--text-secondary);
	}

	.graph-panel {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-sm);
		padding: 0.5rem;
	}

	.graph-canvas {
		width: 100%;
		height: 720px;
	}

	.search-results .result {
		cursor: pointer;
		padding: 0.25rem 0.4rem;
		border-radius: var(--radius-sm);
	}

	.search-results .result:hover {
		background: var(--accent-light);
	}

	@media (max-width: 1024px) {
		.graph-grid {
			grid-template-columns: 1fr;
		}

		.graph-canvas {
			height: 520px;
		}
	}
</style>
