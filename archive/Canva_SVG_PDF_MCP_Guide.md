# Canva SVG-to-PDF MCP Server Integration Guide

## Overview

This guide will help you set up two MCP (Model Context Protocol) servers to enhance your resume workflow:
1. **Official Canva MCP Server** - For professional PDF generation and design automation
2. **File Converter MCP Server** - For SVG-to-PDF conversion capabilities

By the end of this guide, you'll be able to use a prettied-up SVG resume template, convert it to PDF with professional formatting, and automatically upload/manage it through Canva.

## What You'll Achieve

**Current Workflow**: Markdown → Python script → Basic PDF
**New Workflow**: SVG Template → MCP Servers → Professional PDF via Canva → Automated Upload/Management

## Research Findings Summary

### SVG-to-PDF Conversion Options
- **No dedicated SVG-to-PDF MCP server exists yet** (as of 2025)
- **Available alternatives**: General file converters, custom implementations
- **Best current option**: File Converter MCP Server with SVG support

### Canva MCP Server Capabilities
- ✅ **PDF Export**: Direct export of designs as professional PDFs
- ✅ **Template Management**: Autofill templates with your tailored content
- ✅ **Upload/Import**: Import your SVG files and create new designs
- ✅ **No API Key Required**: Uses OAuth authentication (much easier!)
- ✅ **Full Automation**: Create, edit, and export designs programmatically

## Prerequisites

- ✅ Claude Pro subscription (you have this)
- ✅ Claude Desktop installed (you have this)
- ✅ Windows computer (confirmed from your file paths)
- 🔲 Node.js 22.16+ (we'll install this)
- 🔲 Canva account (free or paid)

## Step 1: Install Node.js (Required for MCP Servers)

### 1.1 Download Node.js
1. Open your web browser
2. Go to https://nodejs.org/
3. Click the **green "Download Node.js (LTS)"** button (should show version 22.x or higher)
4. Save the installer file to your Downloads folder

### 1.2 Install Node.js
1. Open your **Downloads** folder
2. **Double-click** the Node.js installer file (e.g., `node-v22.x.x-x64.msi`)
3. Click **"Next"** on the welcome screen
4. Accept the license agreement and click **"Next"**
5. Keep the default installation location and click **"Next"**
6. Keep all default features selected and click **"Next"**
7. Check the box for **"Automatically install the necessary tools"** and click **"Next"**
8. Click **"Install"**
9. When prompted by Windows User Account Control, click **"Yes"**
10. Click **"Finish"** when installation completes

### 1.3 Verify Installation
1. Press **Windows Key + R**
2. Type `cmd` and press **Enter**
3. In the command prompt, type: `node --version`
4. Press **Enter**
5. You should see something like `v22.x.x`
6. Type: `npm --version`
7. Press **Enter**
8. You should see a version number
9. **Close** the command prompt window

## Step 2: Set Up Claude Desktop for MCP Servers

### 2.1 Locate Claude Desktop Configuration
1. Press **Windows Key + R**
2. Type `%APPDATA%` and press **Enter**
3. **Double-click** the **Claude** folder
4. You should see a file called `claude_desktop_config.json`
   - If you don't see this file, create it: **Right-click** → **New** → **Text Document** → Name it `claude_desktop_config.json`

### 2.2 Open Configuration File
1. **Right-click** on `claude_desktop_config.json`
2. Select **"Open with"** → **"Notepad"** (or your preferred text editor)
3. If the file is empty, add this basic structure:
```json
{
  "mcpServers": {}
}
```
4. **Save** the file (**Ctrl + S**)
5. **Keep this file open** - we'll add to it in the next steps

## Step 3: Install Official Canva MCP Server

### 3.1 Add Canva MCP Server via Command Line
1. Press **Windows Key + R**
2. Type `cmd` and press **Enter**
3. In the command prompt, type this exact command:
```bash
npm install -g @canva/mcp
```
4. Press **Enter** and wait for installation to complete
5. **Keep the command prompt open** for the next step

### 3.2 Configure Canva MCP Server
1. Go back to your open `claude_desktop_config.json` file
2. Replace the contents with this configuration:
```json
{
  "mcpServers": {
    "canva": {
      "command": "npx",
      "args": ["@canva/mcp"]
    }
  }
}
```
3. **Save** the file (**Ctrl + S**)

### 3.3 Test Canva MCP Installation
1. In your command prompt, type:
```bash
npx @canva/mcp
```
2. Press **Enter**
3. If successful, you should see MCP server startup messages
4. Press **Ctrl + C** to stop the test
5. **Close** the command prompt

## Step 4: Install File Converter MCP Server

### 4.1 Install File Converter MCP
1. Press **Windows Key + R**
2. Type `cmd` and press **Enter**
3. In the command prompt, type:
```bash
npm install -g file-converter-mcp
```
4. Press **Enter** and wait for installation to complete

### 4.2 Update Configuration File
1. Go back to your `claude_desktop_config.json` file
2. Update it to include both servers:
```json
{
  "mcpServers": {
    "canva": {
      "command": "npx",
      "args": ["@canva/mcp"]
    },
    "file-converter": {
      "command": "npx", 
      "args": ["file-converter-mcp"]
    }
  }
}
```
3. **Save** the file (**Ctrl + S**)
4. **Close** the text editor

## Step 5: Restart Claude Desktop

### 5.1 Restart Claude Desktop
1. **Close** Claude Desktop completely (right-click the system tray icon and select **"Quit"** if it's running)
2. **Wait 5 seconds**
3. **Open** Claude Desktop again from your desktop shortcut or Start menu
4. **Wait** for it to fully load

### 5.2 Verify MCP Servers are Loaded
1. In Claude Desktop, start a new conversation
2. Type: `/mcp`
3. Press **Enter**
4. You should see both **canva** and **file-converter** listed as available MCP servers
5. If you don't see them, restart Claude Desktop again and wait a full minute

## Step 6: Set Up Canva Authentication

### 6.1 Connect to Canva
1. In Claude Desktop, type:
```
Use the Canva MCP server to connect to my Canva account
```
2. Press **Enter**
3. Claude will initiate the OAuth authentication flow
4. A **web browser window** will open automatically
5. **Log in** to your Canva account in the browser
6. Click **"Allow"** or **"Authorize"** when prompted
7. **Close** the browser window when authentication is complete
8. Return to Claude Desktop

### 6.2 Test Canva Connection
1. In Claude Desktop, type:
```
List my existing Canva designs
```
2. Press **Enter**
3. Claude should be able to access and display your Canva designs
4. If this works, your Canva MCP server is properly connected!

## Step 7: Test File Conversion

### 7.1 Test SVG to PDF Conversion
1. Create a simple test SVG file or use an existing one
2. In Claude Desktop, type:
```
Use the file converter MCP to convert my SVG file to PDF
```
3. Follow Claude's prompts to specify the file path
4. Verify that the conversion works properly

## Step 8: Create Your SVG-to-PDF Canva Workflow

### 8.1 End-to-End Workflow Example

Once both servers are working, you can use this workflow:

```
1. Convert SVG resume template to PDF format:
   "Use file-converter MCP to convert resume_template.svg to PDF"

2. Import the PDF into Canva:
   "Use Canva MCP to import the converted PDF as a new design"

3. Customize the design programmatically:
   "Update the Canva design with my tailored resume content for [job title]"

4. Export the final professional PDF:
   "Export the updated Canva design as a high-quality PDF"
```

### 8.2 Automation Possibilities

With both servers configured, you can:
- **Batch convert** multiple SVG resume variations to PDF
- **Automatically import** them into Canva
- **Programmatically update** content based on job descriptions
- **Export professional PDFs** with Canva's advanced formatting
- **Organize designs** in Canva folders for different job applications

## Troubleshooting

### Common Issues and Solutions

**Issue**: "Command not found" when running npm
- **Solution**: Restart your command prompt after installing Node.js

**Issue**: MCP servers don't appear in Claude Desktop
- **Solution**: Check that `claude_desktop_config.json` is in the correct location and has proper JSON syntax

**Issue**: Canva authentication fails
- **Solution**: Make sure you're logged into the correct Canva account in your browser

**Issue**: File conversion doesn't work
- **Solution**: Ensure file paths are correct and files are accessible

**Issue**: JSON configuration file has errors
- **Solution**: Use a JSON validator online to check syntax, ensure all brackets and commas are correct

### Getting Help

1. **Claude Community**: Join the Claude community forums for MCP-related questions
2. **GitHub Issues**: Check the GitHub repositories for each MCP server for known issues
3. **Canva Developers**: Visit https://www.canva.dev/ for Canva MCP specific help

## Advanced Usage

### Custom Styling and Templates

Once you're comfortable with the basic workflow, you can:
1. Create multiple SVG templates for different industries
2. Set up automated styling based on job requirements
3. Use Canva's template library for professional layouts
4. Implement batch processing for multiple job applications

### Integration with Existing Workflow

This new system can work alongside your existing `prompt5.txt` and T-shaped skills system:
1. Use your existing prompt system to generate tailored content
2. Apply that content to your SVG template
3. Process through the new MCP pipeline for professional output
4. Maintain all your existing resume source files and strategies

## Conclusion

You now have a powerful, automated system that can:
- Convert SVG resume templates to professional PDFs
- Leverage Canva's design capabilities through automation
- Maintain the T-shaped skills positioning from your existing system
- Generate multiple professional resume variations quickly

This setup transforms your resume workflow from manual PDF generation to a sophisticated, automated design pipeline that produces professional-quality results.

## Next Steps

1. **Test both servers** thoroughly with simple examples
2. **Create your first SVG resume template** (or convert an existing design)
3. **Practice the complete workflow** with a test job application
4. **Integrate with your existing prompt system** for maximum efficiency
5. **Explore advanced Canva features** available through the MCP server