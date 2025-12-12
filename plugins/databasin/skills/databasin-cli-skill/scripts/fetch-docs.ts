#!/usr/bin/env bun
/**
 * Fetch DataBasin documentation using the databasin docs commands.
 *
 * This script uses the databasin CLI commands to retrieve documentation
 * and saves it to a local references directory for indexing.
 */

import { $ } from "bun";
import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

/**
 * Execute a shell command and return its output
 */
async function runCommand(cmd: string): Promise<string | null> {
	try {
		const result = await $`${cmd}`.text();
		return result;
	} catch (error) {
		console.error(`Error running command: ${cmd}`);
		console.error(`Error: ${error}`);
		return null;
	}
}

/**
 * Fetch all DataBasin documentation and save to output directory
 */
async function fetchAllDocs(outputDir: string): Promise<boolean> {
	await mkdir(outputDir, { recursive: true });

	console.log(`Fetching documentation to ${outputDir}...`);

	// First, get the list of available documentation
	console.log("Getting list of available documentation...");
	const docsListOutput = await runCommand("databasin docs");

	if (!docsListOutput) {
		console.error("Failed to fetch documentation list");
		return false;
	}

	// Save the main docs list
	const mainDocsFile = join(outputDir, "00-documentation-index.md");
	await writeFile(
		mainDocsFile,
		`# DataBasin Documentation Index\n\n${docsListOutput}`
	);
	console.log(`✓ Saved documentation index to ${mainDocsFile}`);

	// Parse the documentation list to find individual doc names
	// This assumes the docs command outputs doc names in a parseable format
	const docNames: string[] = [];
	for (const line of docsListOutput.split("\n")) {
		const trimmed = line.trim();
		if (trimmed && !trimmed.startsWith("#") && !trimmed.startsWith("-")) {
			// Extract doc name - adjust this logic based on actual format
			const parts = trimmed.split(/\s+/);
			if (parts.length > 0) {
				docNames.push(parts[0]);
			}
		}
	}

	// Fetch each individual documentation file
	for (const docName of docNames) {
		if (!docName) continue;

		console.log(`Fetching documentation: ${docName}...`);
		const docContent = await runCommand(`databasin docs ${docName}`);

		if (docContent) {
			// Sanitize filename
			const safeName = docName.replace(/\//g, "-").replace(/\s+/g, "-");
			const docFile = join(outputDir, `${safeName}.md`);

			await writeFile(docFile, `# ${docName}\n\n${docContent}`);
			console.log(`✓ Saved ${docName} to ${docFile}`);
		} else {
			console.error(`✗ Failed to fetch ${docName}`);
		}
	}

	console.log(`\n✅ Documentation fetch complete! Files saved to ${outputDir}`);
	return true;
}

// Main execution
const scriptDir = import.meta.dir;
const skillDir = join(scriptDir, "..");
const defaultOutput = join(skillDir, "references", "databasin-docs");

const outputDir = process.argv[2] || defaultOutput;

const success = await fetchAllDocs(outputDir);
process.exit(success ? 0 : 1);
