/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { spawn } from 'child_process';
import * as path from 'path';

const server = new McpServer({
  name: 'lancedb-server',
  version: '1.0.0',
});

function runLanceDbClient(args: string[]): Promise<any> {
  return new Promise((resolve, reject) => {
    const extensionPath = process.env.GEMINI_EXTENSION_PATH;
    if (!extensionPath) {
      return reject(new Error('GEMINI_EXTENSION_PATH environment variable not set.'));
    }
    const pythonProcess = spawn('python3', [path.join(extensionPath, 'lancedb_client.py'), ...args]);

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`LanceDB client exited with code ${code}: ${stderr}`));
      } else {
        try {
          resolve(JSON.parse(stdout));
        } catch (e) {
          reject(new Error('Failed to parse LanceDB client output as JSON.'));
        }
      }
    });
  });
}

server.registerTool(
  'create_table',
  {
    description: 'Creates a new LanceDB table. If no table name is provided, a default table will be created.',
    inputSchema: z.object({
      tableName: z.string().optional(),
    }).shape,
  },
  async (input) => {
    const args = ['create_table'];
    if (input.tableName) {
      args.push(input.tableName);
    }
    const result = await runLanceDbClient(args);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result),
        },
      ],
    };
  },
);

server.registerTool(
  'add_doc',
  {
    description: 'Adds a document to a LanceDB table. If no table name is provided, the document will be added to a default table.',
    inputSchema: z.object({
      document: z.string(),
      tableName: z.string().optional(),
    }).shape,
  },
  async (input) => {
    const args = ['add_doc', input.document];
    if (input.tableName) {
      args.push('--table_name', input.tableName);
    }
    const result = await runLanceDbClient(args);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result),
        },
      ],
    };
  },
);

server.registerTool(
  'search',
  {
    description: 'Searches for similar documents in a LanceDB table. If no table name is provided, the search will be performed on a default table.',
    inputSchema: z.object({
      query: z.string(),
      tableName: z.string().optional(),
    }).shape,
  },
  async (input) => {
    const args = ['search', input.query];
    if (input.tableName) {
      args.push('--table_name', input.tableName);
    }
    const result = await runLanceDbClient(args);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result),
        },
      ],
    };
  },
);

server.registerTool(
  'delete_table',
  {
    description: 'Deletes a LanceDB table.',
    inputSchema: z.object({
      tableName: z.string(),
    }).shape,
  },
  async (input) => {
    const result = await runLanceDbClient(['delete_table', input.tableName]);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result),
        },
      ],
    };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
