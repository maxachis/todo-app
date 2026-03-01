<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as d3 from 'd3';
	import { api, type GraphData } from '$lib';

	let themeObserver: MutationObserver | null = null;

	let graphEl: HTMLDivElement | null = $state(null);
	let detailsEl: HTMLDivElement | null = $state(null);
	let searchInput: HTMLInputElement | null = $state(null);
	let searchResultsEl: HTMLDivElement | null = $state(null);
	let spacingInput: HTMLInputElement | null = $state(null);
	let repulsionInput: HTMLInputElement | null = $state(null);
	let centeringInput: HTMLInputElement | null = $state(null);
	let hideIsolatedInput: HTMLInputElement | null = $state(null);
	let showEdgeNotesInput: HTMLInputElement | null = $state(null);
	let scaleByConnectionsInput: HTMLInputElement | null = $state(null);
	let showOrgClustersInput: HTMLInputElement | null = $state(null);
	let labelSizeInput: HTMLInputElement | null = $state(null);

	let filterPeople: HTMLInputElement | null = $state(null);
	let filterOrganizations: HTMLInputElement | null = $state(null);
	let filterPersonPerson: HTMLInputElement | null = $state(null);
	let filterOrgPerson: HTMLInputElement | null = $state(null);

	const CLUSTER_COLORS_KEY = 'graph-cluster-colors';
	const DEFAULT_CLUSTER_PALETTE = [
		'#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f',
		'#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac'
	];

	function loadClusterColors(): Record<string, string> {
		if (typeof localStorage === 'undefined') return {};
		try {
			const raw = localStorage.getItem(CLUSTER_COLORS_KEY);
			if (raw) {
				const parsed = JSON.parse(raw);
				if (parsed && typeof parsed === 'object') return parsed;
			}
		} catch {
			// ignore
		}
		return {};
	}

	function saveClusterColors(colors: Record<string, string>): void {
		try {
			if (Object.keys(colors).length === 0) {
				localStorage.removeItem(CLUSTER_COLORS_KEY);
			} else {
				localStorage.setItem(CLUSTER_COLORS_KEY, JSON.stringify(colors));
			}
		} catch {
			// ignore
		}
	}

	let clusterColorMap: Record<string, string> = $state(loadClusterColors());
	let clusterEntries: Array<{ orgId: string; name: string; defaultColor: string }> = $state([]);

	const EDGE_COLORS_KEY = 'graph-edge-colors';

	function loadEdgeColors(): Record<string, string> {
		if (typeof localStorage === 'undefined') return {};
		try {
			const raw = localStorage.getItem(EDGE_COLORS_KEY);
			if (raw) {
				const parsed = JSON.parse(raw);
				if (parsed && typeof parsed === 'object') return parsed;
			}
		} catch {
			// ignore
		}
		return {};
	}

	function saveEdgeColors(colors: Record<string, string>): void {
		try {
			if (Object.keys(colors).length === 0) {
				localStorage.removeItem(EDGE_COLORS_KEY);
			} else {
				localStorage.setItem(EDGE_COLORS_KEY, JSON.stringify(colors));
			}
		} catch {
			// ignore
		}
	}

	function edgeTypeKey(edgeType: string, typeId: number | null): string | null {
		if (typeId == null) return null;
		return edgeType === 'person-person' ? `pp-${typeId}` : `op-${typeId}`;
	}

	function getEdgeColor(
		edgeType: string,
		typeId: number | null,
		colorMap: Record<string, string>,
		fallback: string
	): string {
		const key = edgeTypeKey(edgeType, typeId);
		if (key && colorMap[key]) return colorMap[key];
		return fallback;
	}

	let edgeColorMap: Record<string, string> = $state(loadEdgeColors());
	let edgeTypes: Array<{ key: string; name: string; category: string }> = $state([]);

	onMount(async () => {
		if (!graphEl || !detailsEl) return;
		const raw = await api.graph.get();

		// Focus mode state
		let focusedNodeId: string | null = null;
		let focusDepth: 1 | 2 = 1;
		let focusedNodeData: any = null;

		const renderDetails = (data: any | null) => {
			if (!detailsEl) return;
			if (!data) {
				if (focusedNodeData) {
					renderDetails(focusedNodeData);
					return;
				}
				detailsEl.innerHTML = '<p>Hover over a node to see details.</p>';
				return;
			}
			const title = data.details?.name || data.label || 'Details';
			const type = data.type || 'node';
			const notes = data.details?.notes || '';
			const orgType = data.details?.type || '';
			const isNode = data.type === 'person' || data.type === 'organization';
			const isFocused = focusedNodeId === data.id;
			detailsEl.innerHTML = `
        <div class="space-y-2">
          <div class="text-base font-semibold">${title}</div>
          <div class="text-xs uppercase tracking-wide text-gray-500">${type}</div>
          ${orgType ? `<div class="text-sm"><span class="font-medium">Type:</span> ${orgType}</div>` : ''}
          ${notes ? `<div class="text-sm"><span class="font-medium">Notes:</span> ${notes}</div>` : ''}
          ${isNode ? `<button class="focus-btn">${isFocused ? 'Unfocus' : 'Focus'}</button>` : ''}
          ${isFocused ? `<div class="depth-toggle">
            <label><input type="radio" name="focus-depth" value="1" ${focusDepth === 1 ? 'checked' : ''} /> 1-hop</label>
            <label><input type="radio" name="focus-depth" value="2" ${focusDepth === 2 ? 'checked' : ''} /> 2-hop</label>
          </div>` : ''}
        </div>
      `;
			const focusBtn = detailsEl.querySelector('.focus-btn');
			focusBtn?.addEventListener('click', () => {
				if (isFocused) {
					focusedNodeId = null;
					focusedNodeData = null;
					(graphEl as any)?.__applyFocusOpacity?.();
					renderDetails(null);
				} else {
					focusedNodeId = data.id;
					focusedNodeData = data;
					focusDepth = 1;
					(graphEl as any)?.__applyFocusOpacity?.();
					renderDetails(data);
				}
			});
			if (isFocused) {
				detailsEl.querySelectorAll<HTMLInputElement>('input[name="focus-depth"]').forEach((radio) => {
					radio.addEventListener('change', () => {
						focusDepth = Number(radio.value) as 1 | 2;
						(graphEl as any)?.__applyFocusOpacity?.();
					});
				});
			}
		};

		const renderEdgeDetails = (data: any | null) => {
			if (!detailsEl) return;
			if (!data) {
				renderDetails(null);
				return;
			}
			const type = data.type || 'edge';
			const typeName = data.relationship_type_name || '';
			const notes = data.notes || '';
			detailsEl.innerHTML = `
        <div class="space-y-2">
          <div class="text-base font-semibold">Relationship</div>
          <div class="text-xs uppercase tracking-wide text-gray-500">${type}</div>
          ${typeName ? `<div class="text-sm"><span class="font-medium">Type:</span> ${typeName}</div>` : ''}
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

		const getThemeColors = () => {
			const style = getComputedStyle(document.documentElement);
			return {
				accent: style.getPropertyValue('--accent').trim(),
				textPrimary: style.getPropertyValue('--text-primary').trim(),
				textTertiary: style.getPropertyValue('--text-tertiary').trim(),
				border: style.getPropertyValue('--border').trim()
			};
		};

		const initGraph = (data: GraphData) => {
			if (!graphEl) return;
			const colors = getThemeColors();

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
				notes: edge.data.notes,
				relationship_type_id: edge.data.relationship_type_id,
				relationship_type_name: edge.data.relationship_type_name
			}));

			// Extract distinct relationship types for the color picker
			const typeMap = new Map<string, { key: string; name: string; category: string }>();
			for (const l of links) {
				const key = edgeTypeKey(l.type, l.relationship_type_id);
				if (key && l.relationship_type_name && !typeMap.has(key)) {
					typeMap.set(key, {
						key,
						name: l.relationship_type_name,
						category: l.type === 'person-person' ? 'Person ↔ Person' : 'Org → Person'
					});
				}
			}
			edgeTypes = Array.from(typeMap.values());

			// Build adjacency map from links (before d3 mutates source/target to objects)
			const adjacency = new Map<string, Set<string>>();
			for (const l of links) {
				const src = l.source as string;
				const tgt = l.target as string;
				if (!adjacency.has(src)) adjacency.set(src, new Set());
				if (!adjacency.has(tgt)) adjacency.set(tgt, new Set());
				adjacency.get(src)!.add(tgt);
				adjacency.get(tgt)!.add(src);
			}

			const getNeighborhood = (nodeId: string, depth: 1 | 2): Set<string> => {
				const result = new Set<string>([nodeId]);
				const direct = adjacency.get(nodeId) || new Set();
				for (const n of direct) result.add(n);
				if (depth === 2) {
					for (const n of direct) {
						const secondHop = adjacency.get(n) || new Set();
						for (const nn of secondHop) result.add(nn);
					}
				}
				return result;
			};

			// Build org-cluster map: org ID → member node IDs (org + connected people via org-person edges)
			const orgClusters = new Map<string, string[]>();
			for (const n of nodes) {
				if (n.type === 'organization') {
					const members = [n.id];
					for (const l of links) {
						if (l.type === 'organization-person') {
							const src = l.source as string;
							const tgt = l.target as string;
							if (src === n.id && !members.includes(tgt)) members.push(tgt);
							if (tgt === n.id && !members.includes(src)) members.push(src);
						}
					}
					if (members.length >= 3) {
						orgClusters.set(n.id, members);
					}
				}
			}

			const HULL_PADDING = 15;

			// Populate cluster entries for the color picker UI
			let clusterIdx = 0;
			clusterEntries = [];
			for (const [orgId] of orgClusters) {
				const orgNode = nodes.find((n) => n.id === orgId);
				const defaultColor = DEFAULT_CLUSTER_PALETTE[clusterIdx % DEFAULT_CLUSTER_PALETTE.length];
				clusterEntries.push({
					orgId,
					name: orgNode?.label || orgId,
					defaultColor
				});
				clusterIdx++;
			}

			const getClusterColor = (orgId: string): string => {
				if (clusterColorMap[orgId]) return clusterColorMap[orgId];
				const entry = clusterEntries.find((e) => e.orgId === orgId);
				return entry?.defaultColor || DEFAULT_CLUSTER_PALETTE[0];
			};

			const width = graphEl.clientWidth;
			const height = graphEl.clientHeight;

			const svg = d3
				.select(graphEl)
				.append('svg')
				.attr('viewBox', [0, 0, width, height])
				.attr('class', 'w-full h-full');

			const zoomLayer = svg.append('g').attr('class', 'zoom-layer');
			const hullGroup = zoomLayer.append('g').attr('class', 'hulls');
			const linkGroup = zoomLayer.append('g').attr('class', 'links');
			const linkLabelGroup = zoomLayer.append('g').attr('class', 'link-labels');
			const nodeGroup = zoomLayer.append('g').attr('class', 'nodes');
			const labelGroup = zoomLayer.append('g').attr('class', 'labels');

			const zoom = d3.zoom<SVGSVGElement, unknown>().scaleExtent([0.3, 3]).on('zoom', (event) => {
				zoomLayer.attr('transform', event.transform);
			});

			svg.call(zoom);

			// Canvas click to exit focus mode (ignore drags/pans)
			let isDragging = false;
			svg.on('pointerdown.focustracker', () => {
				isDragging = false;
			});
			svg.on('pointermove.focustracker', () => {
				isDragging = true;
			});
			svg.on('click.focus', (event) => {
				if (isDragging) return;
				const target = event.target as Element;
				if (
					target.tagName === 'svg' ||
					(target.tagName === 'g' && target.classList.contains('zoom-layer'))
				) {
					if (focusedNodeId) {
						focusedNodeId = null;
						focusedNodeData = null;
						applyFocusOpacity();
						updateHulls();
						renderDetails(null);
					}
				}
			});

			const linkForce = d3.forceLink(links).id((d: any) => d.id).distance(140);
			const chargeForce = d3.forceManyBody().strength(-500);
			const collideForce = d3.forceCollide(18);

			const computeConnectionCounts = (edges: any[]): Map<string, number> => {
				const counts = new Map<string, number>();
				for (const e of edges) {
					if (e.hidden) continue;
					const src = e.source.id || e.source;
					const tgt = e.target.id || e.target;
					counts.set(src, (counts.get(src) || 0) + 1);
					counts.set(tgt, (counts.get(tgt) || 0) + 1);
				}
				return counts;
			};

			const scaledRadius = (count: number, maxCount: number): number => {
				const MIN_R = 5;
				const MAX_R = 20;
				if (maxCount <= 0) return MAX_R;
				return MIN_R + (count / maxCount) * (MAX_R - MIN_R);
			};

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
				.attr('stroke', (d: any) =>
					getEdgeColor(d.type, d.relationship_type_id, edgeColorMap, colors.border)
				)
				.attr('stroke-width', 1.5)
				.on('mouseenter', (_event, d: any) => renderEdgeDetails(d))
				.on('mouseleave', () => renderDetails(null));

			const linkLabels = linkLabelGroup
				.selectAll('text')
				.data(links, (d: any) => d.id)
				.join('text')
				.text((d: any) => d.notes || '')
				.attr('font-size', 10)
				.attr('fill', colors.textTertiary)
				.attr('text-anchor', 'middle')
				.attr('dy', -4)
				.attr('display', 'none');

			const node = nodeGroup
				.selectAll('circle')
				.data(nodes, (d: any) => d.id)
				.join('circle')
				.attr('r', (d: any) => (d.type === 'organization' ? 9 : 7))
				.attr('fill', (d: any) => (d.type === 'organization' ? colors.accent : colors.textTertiary))
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
				.on('mouseleave', () => renderDetails(null))
				.on('click', (_event, d: any) => {
					if (focusedNodeId === d.id) {
						focusedNodeId = null;
						focusedNodeData = null;
					} else {
						focusedNodeId = d.id;
						focusedNodeData = d;
						focusDepth = 1;
					}
					applyFocusOpacity();
					updateHulls();
					renderDetails(focusedNodeData);
				});

			const labels = labelGroup
				.selectAll('text')
				.data(nodes, (d: any) => d.id)
				.join('text')
				.text((d: any) => d.label)
				.attr('font-size', 11)
				.attr('fill', colors.textPrimary)
				.attr('text-anchor', 'middle')
				.attr('dy', -12);

			const updateNodeSizes = () => {
				const enabled = scaleByConnectionsInput?.checked ?? false;
				if (enabled) {
					const counts = computeConnectionCounts(links);
					const maxCount = Math.max(...counts.values(), 0);
					node.attr('r', (d: any) => scaledRadius(counts.get(d.id) || 0, maxCount));
					collideForce.radius((d: any) => scaledRadius(counts.get(d.id) || 0, maxCount) + 4);
				} else {
					node.attr('r', (d: any) => (d.type === 'organization' ? 9 : 7));
					collideForce.radius(18);
				}
				simulation.alpha(0.3).restart();
			};

			const refreshVisibility = () => {
				applyFilters(nodes, links);
				node.attr('display', (d: any) => (d.hidden ? 'none' : 'block'));
				labels.attr('display', (d: any) => (d.hidden ? 'none' : 'block'));
				link.attr('display', (d: any) => (d.hidden ? 'none' : 'block'));
				linkLabels.attr('display', (d: any) => {
					if (d.hidden) return 'none';
					return showEdgeNotesInput?.checked ? 'block' : 'none';
				});
				updateNodeSizes();
				updateHulls();
				applyFocusOpacity();
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
							searchResultsEl!.textContent = '';
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

			simulation.on('tick', () => {
				updatePositions();
				updateHulls();
			});

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
			attachInput(scaleByConnectionsInput);
			attachInput(showOrgClustersInput);
			attachInput(spacingInput);
			attachInput(repulsionInput);
			attachInput(centeringInput);
			attachInput(labelSizeInput);

			searchInput?.addEventListener('input', search);

			const updateColors = () => {
				const c = getThemeColors();
				Object.assign(colors, c);
				node.attr('fill', (d: any) => (d.type === 'organization' ? c.accent : c.textTertiary));
				labels.attr('fill', c.textPrimary);
				link.attr('stroke', (d: any) =>
					getEdgeColor(d.type, d.relationship_type_id, edgeColorMap, c.border)
				);
				linkLabels.attr('fill', c.textTertiary);
				hullGroup.selectAll<SVGPathElement, { orgId: string }>('path')
					.attr('fill', (d) => getClusterColor(d.orgId))
					.attr('stroke', (d) => getClusterColor(d.orgId));
			};

			const applyEdgeColor = (typeKey: string, color: string) => {
				edgeColorMap[typeKey] = color;
				edgeColorMap = { ...edgeColorMap };
				saveEdgeColors(edgeColorMap);
				updateColors();
			};

			const resetEdgeColors = () => {
				edgeColorMap = {};
				saveEdgeColors(edgeColorMap);
				updateColors();
			};

			// Expose functions for the template
			(graphEl as any).__applyEdgeColor = applyEdgeColor;
			(graphEl as any).__resetEdgeColors = resetEdgeColors;

			const applyFocusOpacity = () => {
				// Focus ring on the focused node
				node.attr('stroke', (d: any) => (d.id === focusedNodeId ? colors.textPrimary : null))
					.attr('stroke-width', (d: any) => (d.id === focusedNodeId ? 2.5 : null));

				if (!focusedNodeId) {
					node.attr('opacity', null);
					labels.attr('opacity', null);
					link.attr('opacity', null);
					linkLabels.attr('opacity', null);
					hullGroup.selectAll('path').attr('opacity', null);
					return;
				}
				const neighborhood = getNeighborhood(focusedNodeId, focusDepth);
				node.attr('opacity', (d: any) =>
					d.hidden ? null : neighborhood.has(d.id) ? 1 : 0.08
				);
				labels.attr('opacity', (d: any) =>
					d.hidden ? null : neighborhood.has(d.id) ? 1 : 0.08
				);
				link.attr('opacity', (d: any) => {
					if (d.hidden) return null;
					const srcId = d.source.id || d.source;
					const tgtId = d.target.id || d.target;
					return neighborhood.has(srcId) && neighborhood.has(tgtId) ? 1 : 0.08;
				});
				linkLabels.attr('opacity', (d: any) => {
					if (d.hidden) return null;
					const srcId = d.source.id || d.source;
					const tgtId = d.target.id || d.target;
					return neighborhood.has(srcId) && neighborhood.has(tgtId) ? 1 : 0.08;
				});
				hullGroup.selectAll('path').attr('opacity', (d: any) =>
					neighborhood.has(d.orgId) ? 1 : 0.08
				);
			};

			const updateHulls = () => {
				const visible = showOrgClustersInput?.checked ?? true;
				hullGroup.attr('display', visible ? null : 'none');
				if (!visible) return;

				const hullData: Array<{ orgId: string; hull: [number, number][] }> = [];
				for (const [orgId, memberIds] of orgClusters) {
					const points: [number, number][] = [];
					for (const id of memberIds) {
						const n = (nodes as any[]).find((nd) => nd.id === id);
						if (n && n.x != null && n.y != null && !n.hidden) {
							for (let a = 0; a < Math.PI * 2; a += Math.PI / 4) {
								points.push([
									n.x + HULL_PADDING * Math.cos(a),
									n.y + HULL_PADDING * Math.sin(a)
								]);
							}
						}
					}
					if (points.length >= 6) {
						const hull = d3.polygonHull(points);
						if (hull) hullData.push({ orgId, hull });
					}
				}

				const paths = hullGroup
					.selectAll<SVGPathElement, { orgId: string; hull: [number, number][] }>('path')
					.data(hullData, (d) => d.orgId);
				paths.exit().remove();
				const entered = paths.enter().append('path');
				entered
					.merge(paths)
					.attr('fill', (d) => getClusterColor(d.orgId))
					.attr('fill-opacity', 0.1)
					.attr('stroke', (d) => getClusterColor(d.orgId))
					.attr('stroke-opacity', 0.2)
					.attr('stroke-width', 1)
					.attr('d', (d) => `M${d.hull.map((p) => p.join(',')).join('L')}Z`)
					.attr('opacity', (d) => {
						if (!focusedNodeId) return 1;
						const neighborhood = getNeighborhood(focusedNodeId, focusDepth);
						return neighborhood.has(d.orgId) ? 1 : 0.08;
					});
			};

			const applyClusterColor = (orgId: string, color: string) => {
				clusterColorMap[orgId] = color;
				clusterColorMap = { ...clusterColorMap };
				saveClusterColors(clusterColorMap);
				updateHulls();
			};

			const resetClusterColors = () => {
				clusterColorMap = {};
				saveClusterColors(clusterColorMap);
				updateHulls();
			};

			(graphEl as any).__applyClusterColor = applyClusterColor;
			(graphEl as any).__resetClusterColors = resetClusterColors;
			(graphEl as any).__applyFocusOpacity = applyFocusOpacity;

			themeObserver = new MutationObserver((mutations) => {
				for (const m of mutations) {
					if (m.attributeName === 'data-theme') {
						updateColors();
						break;
					}
				}
			});
			themeObserver.observe(document.documentElement, { attributes: true });

			refreshVisibility();
		};

		initGraph(raw);
	});

	onDestroy(() => {
		themeObserver?.disconnect();
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
					<label><input type="checkbox" bind:this={scaleByConnectionsInput} /> Scale nodes by connections</label>
					<label><input type="checkbox" bind:this={showOrgClustersInput} checked /> Show org clusters</label>
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
				<h2>Edge Colors</h2>
				<div class="stack">
					{#if edgeTypes.length === 0}
						<p class="hint">No relationship types available.</p>
					{:else}
						{#each edgeTypes as et (et.key)}
							<div class="color-row">
								<input
									type="color"
									value={edgeColorMap[et.key] || '#888888'}
									oninput={(e) => {
										const color = (e.target as HTMLInputElement).value;
										(graphEl as any)?.__applyEdgeColor?.(et.key, color);
									}}
								/>
								<span class="color-label">{et.name}</span>
								<span class="color-category">{et.category}</span>
							</div>
						{/each}
						<button
							class="reset-btn"
							onclick={() => {
								(graphEl as any)?.__resetEdgeColors?.();
							}}
						>
							Reset
						</button>
					{/if}
				</div>
			</div>

			<div class="card">
				<h2>Cluster Colors</h2>
				<div class="stack">
					{#if clusterEntries.length === 0}
						<p class="hint">No org clusters available.</p>
					{:else}
						{#each clusterEntries as ce (ce.orgId)}
							<div class="color-row">
								<input
									type="color"
									value={clusterColorMap[ce.orgId] || ce.defaultColor}
									oninput={(e) => {
										const color = (e.target as HTMLInputElement).value;
										(graphEl as any)?.__applyClusterColor?.(ce.orgId, color);
									}}
								/>
								<span class="color-label">{ce.name}</span>
							</div>
						{/each}
						<button
							class="reset-btn"
							onclick={() => {
								(graphEl as any)?.__resetClusterColors?.();
							}}
						>
							Reset
						</button>
					{/if}
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

	.details :global(.focus-btn) {
		margin-top: 0.25rem;
		padding: 0.3rem 0.6rem;
		font-size: 0.8rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--bg-surface);
		color: var(--text-secondary);
		cursor: pointer;
		font-family: var(--font-body);
	}

	.details :global(.focus-btn:hover) {
		background: var(--bg-page);
	}

	.details :global(.depth-toggle) {
		display: flex;
		gap: 0.75rem;
		font-size: 0.8rem;
		color: var(--text-secondary);
		margin-top: 0.25rem;
	}

	.details :global(.depth-toggle label) {
		display: flex;
		align-items: center;
		gap: 0.25rem;
		cursor: pointer;
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

	.hint {
		margin: 0;
		color: var(--text-tertiary);
		font-size: 0.8rem;
	}

	.color-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.color-row input[type='color'] {
		width: 28px;
		height: 28px;
		padding: 0;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		cursor: pointer;
		background: none;
		flex-shrink: 0;
	}

	.color-label {
		flex: 1;
		font-size: 0.85rem;
		color: var(--text-primary);
	}

	.color-category {
		font-size: 0.7rem;
		color: var(--text-tertiary);
		white-space: nowrap;
	}

	.reset-btn {
		margin-top: 0.25rem;
		padding: 0.3rem 0.6rem;
		font-size: 0.8rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--bg-surface);
		color: var(--text-secondary);
		cursor: pointer;
		font-family: var(--font-body);
	}

	.reset-btn:hover {
		background: var(--bg-page);
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
