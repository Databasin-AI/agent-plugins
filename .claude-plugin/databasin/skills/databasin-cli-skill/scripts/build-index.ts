#!/usr/bin/env bun
/**
 * Build a consolidated index of DataBasin documentation with line numbers and descriptions.
 *
 * Creates a low-token, searchable index that maps topics to file locations with line numbers.
 */

import { readdir, readFile, writeFile, mkdir } from "node:fs/promises";
import { join, relative } from "node:path";

interface IndexEntry {
	title: string;
	level: number;
	line: number;
	file: string;
	contentPreview: string;
	category: string;
	relativePath: string;
}

/**
 * Extract headers and their line numbers from a markdown file
 */
async function extractHeadersAndContent(filePath: string): Promise<Omit<IndexEntry, 'category' | 'relativePath'>[]> {
	const content = await readFile(filePath, "utf-8");
	const lines = content.split("\n");
	const entries: Omit<IndexEntry, 'category' | 'relativePath'>[] = [];

	let currentSection: Omit<IndexEntry, 'category' | 'relativePath'> | null = null;

	for (let i = 0; i < lines.length; i++) {
		const line = lines[i];
		const lineNum = i + 1;

		// Match markdown headers (# Header, ## Header, etc.)
		const headerMatch = line.trim().match(/^(#{1,6})\s+(.+)$/);

		if (headerMatch) {
			const level = headerMatch[1].length;
			const title = headerMatch[2].trim();

			// Save previous section if exists
			if (currentSection) {
				entries.push(currentSection);
			}

			// Start new section
			currentSection = {
				title,
				level,
				line: lineNum,
				file: filePath,
				contentPreview: "",
			};
		} else if (currentSection && line.trim()) {
			// Collect first few non-empty lines as preview (max 200 chars)
			if (currentSection.contentPreview.length < 200) {
				currentSection.contentPreview += " " + line.trim();
			}
		}
	}

	// Add the last section
	if (currentSection) {
		entries.push(currentSection);
	}

	return entries;
}

/**
 * Determine the category/module for a documentation file
 */
function categorizeFile(filePath: string): string {
	const pathStr = filePath.toLowerCase();

	// Map file paths to modules
	if (pathStr.includes("flowbasin") || pathStr.includes("pipeline")) {
		return "Flowbasin";
	} else if (
		pathStr.includes("lakebasin") ||
		pathStr.includes("query") ||
		pathStr.includes("trino")
	) {
		return "Lakebasin";
	} else if (
		pathStr.includes("reportbasin") ||
		pathStr.includes("report") ||
		pathStr.includes("llm")
	) {
		return "Reportbasin";
	} else if (pathStr.includes("api")) {
		return "API";
	} else if (
		pathStr.includes("frontend") ||
		pathStr.includes("svelte") ||
		pathStr.includes("component")
	) {
		return "Frontend";
	} else if (
		pathStr.includes("backend") ||
		pathStr.includes("scala") ||
		pathStr.includes("controller")
	) {
		return "Backend";
	} else if (pathStr.includes("connector") || pathStr.includes("cdata")) {
		return "Connectors";
	} else if (pathStr.includes("auth") || pathStr.includes("security")) {
		return "Authentication";
	} else if (pathStr.includes("config") || pathStr.includes("setup")) {
		return "Configuration";
	} else {
		return "General";
	}
}

/**
 * Recursively find all markdown files in a directory
 */
async function findMarkdownFiles(dir: string): Promise<string[]> {
	const files: string[] = [];

	async function traverse(currentDir: string) {
		const entries = await readdir(currentDir, { withFileTypes: true });

		for (const entry of entries) {
			const fullPath = join(currentDir, entry.name);

			if (entry.isDirectory()) {
				await traverse(fullPath);
			} else if (entry.isFile() && entry.name.endsWith(".md")) {
				files.push(fullPath);
			}
		}
	}

	await traverse(dir);
	return files;
}

/**
 * Build a consolidated index from all documentation files
 */
async function buildIndex(docsDir: string, outputFile: string): Promise<boolean> {
	try {
		console.log(`Building index from ${docsDir}...`);

		// Collect all markdown files
		const mdFiles = await findMarkdownFiles(docsDir);

		if (mdFiles.length === 0) {
			console.error(`Warning: No markdown files found in ${docsDir}`);
			return false;
		}

		console.log(`Found ${mdFiles.length} documentation files`);

		// Extract entries from all files
		const allEntries: IndexEntry[] = [];

		for (const mdFile of mdFiles) {
			const category = categorizeFile(mdFile);
			const entries = await extractHeadersAndContent(mdFile);

			for (const entry of entries) {
				allEntries.push({
					...entry,
					category,
					relativePath: relative(docsDir, mdFile),
				});
			}
		}

		console.log(`Extracted ${allEntries.length} documentation sections`);

		// Group entries by category
		const categories: Record<string, IndexEntry[]> = {};
		for (const entry of allEntries) {
			if (!categories[entry.category]) {
				categories[entry.category] = [];
			}
			categories[entry.category].push(entry);
		}

		// Write the consolidated index
		const outputDir = join(outputFile, "..");
		await mkdir(outputDir, { recursive: true });

		let indexContent = "# DataBasin Documentation Index\n\n";
		indexContent += "Quick reference index for DataBasin documentation with file locations and line numbers.\n\n";
		indexContent += `**Total sections indexed:** ${allEntries.length}\n\n`;
		indexContent += "---\n\n";

		// Write table of contents
		indexContent += "## Table of Contents\n\n";
		for (const category of Object.keys(categories).sort()) {
			const anchor = category.toLowerCase().replace(/\s+/g, "-");
			indexContent += `- [${category}](#${anchor}) (${categories[category].length} sections)\n`;
		}
		indexContent += "\n---\n\n";

		// Write each category
		for (const category of Object.keys(categories).sort()) {
			indexContent += `## ${category}\n\n`;

			const sortedEntries = categories[category].sort((a, b) => {
				const pathCompare = a.relativePath.localeCompare(b.relativePath);
				return pathCompare !== 0 ? pathCompare : a.line - b.line;
			});

			for (const entry of sortedEntries) {
				indexContent += `### ${entry.title}\n\n`;
				indexContent += `**Location:** \`${entry.relativePath}:${entry.line}\`\n\n`;

				// Add content preview if available
				let preview = entry.contentPreview.trim();
				if (preview) {
					// Limit preview to first sentence or 150 chars
					if (preview.length > 150) {
						preview = preview.substring(0, 147) + "...";
					}
					indexContent += `**Description:** ${preview}\n\n`;
				}

				indexContent += "---\n\n";
			}
		}

		await writeFile(outputFile, indexContent);

		console.log(`✅ Index built successfully: ${outputFile}`);
		console.log(`   Total categories: ${Object.keys(categories).length}`);
		console.log(`   Total sections: ${allEntries.length}`);

		return true;
	} catch (error) {
		console.error(`Error building index: ${error}`);
		return false;
	}
}

// Main execution
const scriptDir = import.meta.dir;
const skillDir = join(scriptDir, "..");
const defaultDocsDir = join(skillDir, "references", "databasin-docs");
const defaultOutput = join(skillDir, "references", "documentation-index.md");

const docsDir = process.argv[2] || defaultDocsDir;
const outputFile = process.argv[3] || defaultOutput;

const success = await buildIndex(docsDir, outputFile);
process.exit(success ? 0 : 1);
