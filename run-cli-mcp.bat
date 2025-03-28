@echo off
npx -y @smithery/cli@latest run cli-mcp-server --cline "{\"allowedDir\":\"L:\\\",\"allowedCommands\":\"ls,cat,pwd\",\"allowedFlags\":\"-l,-a,--help\",\"commandTimeout\":30,\"maxCommandLength\":1024}"
