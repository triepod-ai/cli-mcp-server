# CLI-MCP-Server Configuration Guide

This guide explains the issues with the current configuration and provides recommended solutions for properly configuring the cli-mcp-server in your MCP server setup.

## Current Configuration Issues

Your current configuration in `cline_mcp_settings.json` has several issues:

1. **Implementation Mismatch**: The server is configured to run through PowerShell using npx with @smithery/cli, but the actual implementation is a Python-based MCP server.

2. **Security Configuration Mismatch**: The JSON configuration string passed to the CLI doesn't match the security model of the actual implementation.

3. **Path Validation Issues**: The first entry in `allowedDir` is a file path (`L:\\ToolNexusMCP_plugins\\mcp-core\\dist\\index.js`) rather than a directory, which could cause issues with the server's path validation logic.

4. **Configuration Method**: Using a complex JSON string in PowerShell arguments is error-prone and difficult to maintain.

## Recommended Solutions

We've created two configuration files with corrected settings:

### 1. Production Configuration (`recommended_mcp_config.json`)

```json
{
  "mcpServers": {
    "cli-mcp-server": {
      "command": "uvx",
      "args": [
        "cli-mcp-server"
      ],
      "env": {
        "ALLOWED_DIR": "L:\\",
        "ALLOWED_COMMANDS": "ls,cat,pwd,Get-ChildItem,Get-Content,Set-Location,Get-Location,Select-Object,Where-Object,Sort-Object,Measure-Object,ForEach-Object,Format-Table,Format-List,ConvertTo-Json,ConvertFrom-Json,Export-Csv,Import-Csv,Test-Path",
        "ALLOWED_FLAGS": "-l,-a,--help,-Force,-Recurse,-Path,-Filter,-ErrorAction,-ErrorVariable",
        "MAX_COMMAND_LENGTH": "2048",
        "COMMAND_TIMEOUT": "60"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

This configuration:
- Uses `uvx` to run the published package
- Sets appropriate environment variables to configure the server
- Includes PowerShell-specific commands and flags

### 2. Development Configuration (`recommended_dev_mcp_config.json`)

```json
{
  "mcpServers": {
    "cli-mcp-server": {
      "command": "uv",
      "args": [
        "--directory", 
        "L:/ToolNexusMCP_plugins/cli-mcp-server",
        "run",
        "cli-mcp-server"
      ],
      "env": {
        "ALLOWED_DIR": "L:\\",
        "ALLOWED_COMMANDS": "ls,cat,pwd,Get-ChildItem,Get-Content,Set-Location,Get-Location,Select-Object,Where-Object,Sort-Object,Measure-Object,ForEach-Object,Format-Table,Format-List,ConvertTo-Json,ConvertFrom-Json,Export-Csv,Import-Csv,Test-Path",
        "ALLOWED_FLAGS": "-l,-a,--help,-Force,-Recurse,-Path,-Filter,-ErrorAction,-ErrorVariable",
        "MAX_COMMAND_LENGTH": "2048",
        "COMMAND_TIMEOUT": "60"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

This configuration:
- Uses `uv` with the `--directory` option to run the package directly from the development directory
- Ideal for testing and development

## Updated `config.json`

We've also updated the local `config.json` file to match the environment variables in the MCP configuration:

```json
{
  "allowedDir": "L:\\",
  "allowedCommands": "ls,cat,pwd,Get-ChildItem,Get-Content,Set-Location,Get-Location,Select-Object,Where-Object,Sort-Object,Measure-Object,ForEach-Object,Format-Table,Format-List,ConvertTo-Json,ConvertFrom-Json,Export-Csv,Import-Csv,Test-Path",
  "allowedFlags": "-l,-a,--help,-Force,-Recurse,-Path,-Filter,-ErrorAction,-ErrorVariable",
  "commandTimeout": 60,
  "maxCommandLength": 2048
}
```

## How to Apply the Configuration

To use one of these configurations:

1. Open your Claude settings file located at:
   `c:\Users\bthom\AppData\Roaming\Windsurf\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`

2. Copy and paste the content from either `recommended_mcp_config.json` (production) or `recommended_dev_mcp_config.json` (development) into the file.

3. If the file already contains other MCP server configurations, make sure to only replace the `cli-mcp-server` section within the `mcpServers` object.

## Security Considerations

- The `ALLOWED_DIR` setting is critical for security as it restricts where commands can be executed.
- The `ALLOWED_COMMANDS` list should only include commands that are necessary for your use case.
- Setting `commandTimeout` helps prevent long-running or hanging commands.
- Review the allowed flags to ensure they don't introduce security risks.

## Troubleshooting

If you encounter issues:

1. Check that the paths in the configuration exist on your system.
2. Verify that `uv` or `uvx` is installed and accessible in your PATH.
3. Use the MCP Inspector for debugging as mentioned in the README:
   ```bash
   npx @modelcontextprotocol/inspector uv --directory L:/ToolNexusMCP_plugins/cli-mcp-server run cli-mcp-server
   ```
4. If using `uvx`, make sure the package is installed globally or in your PATH.
