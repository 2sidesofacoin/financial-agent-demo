"""
Interactive streaming example demonstrating real-time Bigdata search workflow.

This example shows how to:
1. Use multiple stream modes for comprehensive progress monitoring
2. Display live progress indicators and ASCII dashboards
3. Show real-time API execution status and performance metrics
4. Stream token-by-token report generation

Usage:
    python -m bigdata_search.streaming_example
"""

import asyncio
import os
import time
import logging
import warnings
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Suppress warnings and gRPC messages for clean output
warnings.filterwarnings('ignore')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Configure logging to suppress unwanted messages
logging.getLogger('google').setLevel(logging.ERROR)
logging.getLogger('google.auth').setLevel(logging.ERROR)
logging.getLogger('google.generativeai').setLevel(logging.ERROR)

from bigdata_search import (
    bigdata_search_graph,
    BigdataSearchConfiguration,
)

# Rich imports for beautiful output
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.columns import Columns
from rich import box

class StreamingProgressMonitor:
    """Enhanced progress monitor for the streaming workflow with Rich formatting."""
    
    def __init__(self):
        self.start_time = time.time()
        self.search_status = {}
        self.overall_progress = {
            "planning": "⏳ Pending",
            "searching": "⏳ Pending", 
            "gathering": "⏳ Pending",
            "compiling": "⏳ Pending"
        }
        self.console = Console()
        self.progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TimeElapsedColumn(),
            console=self.console
        )
        self.overall_task = None
        
    def print_header(self):
        """Print beautiful Rich header."""
        header_text = Text("🔍 BIGDATA INTERACTIVE SEARCH WORKFLOW", style="bold cyan")
        subtitle_text = Text("Real-time streaming demonstration", style="italic")
        
        header_panel = Panel(
            Text.assemble(header_text, "\n", subtitle_text),
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(header_panel)
        
    def start_progress(self):
        """Initialize the Rich progress bar."""
        self.progress.start()
        self.overall_task = self.progress.add_task("Overall Progress", total=4)
        
    def update_progress(self, completed_steps: int):
        """Update the Rich progress bar."""
        if self.overall_task is not None:
            self.progress.update(self.overall_task, completed=completed_steps)
        
    def stop_progress(self):
        """Stop the Rich progress bar."""
        self.progress.stop()
        
    def create_status_table(self):
        """Create a Rich table for status dashboard."""
        table = Table(title="📋 Workflow Status Dashboard", box=box.ROUNDED)
        table.add_column("Stage", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")
        
        for stage, status in self.overall_progress.items():
            table.add_row(stage.capitalize(), status)
            
        return table
    
    def create_search_status_table(self):
        """Create a Rich table for search execution status."""
        if not self.search_status:
            return None
            
        table = Table(title="🔍 Search Execution Status", box=box.ROUNDED)
        table.add_column("Tool Type", style="green", no_wrap=True)
        table.add_column("Status", style="yellow")
        
        for tool_type, status in self.search_status.items():
            table.add_row(tool_type.upper(), status)
            
        return table
        
    def print_status_dashboard(self):
        """Print beautiful Rich status dashboard."""
        status_table = self.create_status_table()
        search_table = self.create_search_status_table()
        
        if search_table:
            tables = Columns([status_table, search_table], equal=True, expand=True)
            self.console.print(tables)
        else:
            self.console.print(status_table)
        
    def update_stage(self, stage: str, status: str):
        """Update overall workflow stage status."""
        if stage in self.overall_progress:
            self.overall_progress[stage] = status
            
    def update_search_status(self, tool_type: str, status: str):
        """Update individual search status."""
        self.search_status[tool_type] = status
        
    def print_message(self, message: str, style: str = "default"):
        """Print a styled message using Rich."""
        self.console.print(message, style=style)
        
    def print_success(self, message: str):
        """Print a success message."""
        self.console.print(f"✅ {message}", style="bold green")
        
    def print_error(self, message: str):
        """Print an error message."""
        self.console.print(f"❌ {message}", style="bold red")
        
    def print_info(self, message: str):
        """Print an info message."""
        self.console.print(f"ℹ️  {message}", style="cyan")
        
    def print_warning(self, message: str):
        """Print a warning message."""
        self.console.print(f"⚠️  {message}", style="yellow")

async def handle_custom_stream(chunk, monitor):
    """Handle custom stream events with Rich formatting."""
    chunk_type = chunk.get("type", "unknown")
    message = chunk.get("message", "")
    
    # Planning phase events
    if chunk_type == "planning_start":
        monitor.update_stage("planning", "🧠 Analyzing...")
        monitor.console.print(f"\n{message}", style="bold blue")
        
    elif chunk_type == "planning_config":
        monitor.console.print(f"  {message}", style="cyan")
        
    elif chunk_type == "planning_model":
        monitor.console.print(f"  {message}", style="dim cyan")
        
    elif chunk_type == "planning_thinking":
        monitor.console.print(f"  {message}", style="magenta")
        
    elif chunk_type == "strategy_preview":
        strategy_panel = Panel(
            message.replace("📊 Strategy ", "Strategy "),
            title=f"Strategy {chunk.get('strategy_index', '?')}",
            border_style="green",
            padding=(0, 1)
        )
        monitor.console.print(strategy_panel)
        
    elif chunk_type == "query_preview":
        monitor.console.print(f"    {message}", style="dim green")
        
    elif chunk_type == "planning_ready":
        monitor.update_stage("planning", "✅ Complete")
        monitor.print_success(message.replace("🚀 ", ""))
        
    # Search execution events
    elif chunk_type == "search_start":
        tool_type = chunk.get("tool_type", "unknown")
        monitor.update_stage("searching", "🔍 Executing...")
        monitor.update_search_status(tool_type, "⏳ Starting...")
        search_panel = Panel(
            message,
            title=f"Starting {tool_type.upper()} Search",
            border_style="yellow",
            padding=(0, 1)
        )
        monitor.console.print(search_panel)
        
    elif chunk_type == "api_start":
        tool_type = chunk.get("tool_type", "unknown")
        monitor.update_search_status(tool_type, "🚀 API Call...")
        monitor.console.print(f"  {message}", style="yellow")
        
    elif chunk_type == "api_success":
        tool_type = chunk.get("tool_type", "unknown")
        execution_time = chunk.get("execution_time", 0)
        monitor.update_search_status(tool_type, f"✅ Done ({execution_time:.1f}s)")
        monitor.print_success(message.replace("✅ ", ""))
        
    elif chunk_type == "result_quality":
        quality = chunk.get("quality", "🟡 Medium")
        content_length = chunk.get("content_length", 0)
        quality_text = Text(f"  📊 Result quality: {quality} ({content_length:,} chars)")
        
        # Color based on quality
        if "🟢" in quality:
            quality_text.stylize("bold green")
        elif "🟡" in quality:
            quality_text.stylize("bold yellow") 
        elif "🔴" in quality:
            quality_text.stylize("bold red")
            
        monitor.console.print(quality_text)
        
    elif chunk_type == "api_error":
        tool_type = chunk.get("tool_type", "unknown")
        monitor.update_search_status(tool_type, "❌ Failed")
        monitor.print_error(message.replace("❌ ", ""))
        
    elif chunk_type == "search_complete":
        tool_type = chunk.get("tool_type", "unknown")
        success = chunk.get("success", False)
        status = "✅ Success" if success else "❌ Failed"
        monitor.update_search_status(tool_type, status)
        
    # Gathering phase events
    elif chunk_type == "gathering_start":
        monitor.update_stage("searching", "✅ Complete")
        monitor.update_stage("gathering", "📊 Processing...")
        monitor.console.print(f"\n{message}", style="bold magenta")
        
    elif chunk_type == "success_analysis":
        monitor.console.print(f"  {message}", style="green")
        
    elif chunk_type == "performance_metrics":
        monitor.console.print(f"  {message}", style="cyan")
        
    elif chunk_type == "gathering_complete":
        monitor.update_stage("gathering", "✅ Complete")
        monitor.print_success(message.replace("✅ ", ""))
        
    # Compilation phase events
    elif chunk_type == "compilation_start":
        monitor.update_stage("compiling", "📝 Writing...")
        monitor.console.print(f"\n{message}", style="bold green")
        
    elif chunk_type == "synthesis_start":
        monitor.console.print(f"  {message}", style="magenta")
        
    elif chunk_type == "synthesis_complete":
        synthesis_time = chunk.get("synthesis_time", 0)
        report_length = chunk.get("report_length", 0)
        monitor.print_success(message.replace("✅ ", ""))
        
    elif chunk_type == "report_stats":
        monitor.console.print(f"  {message}", style="cyan")
        
    elif chunk_type == "workflow_complete":
        monitor.update_stage("compiling", "✅ Complete")
        total_time = chunk.get("total_time", 0)
        
        completion_panel = Panel(
            f"{message}\n🕐 Total execution time: {total_time:.1f} seconds",
            title="🎉 Workflow Complete",
            border_style="bright_green",
            padding=(1, 2)
        )
        monitor.console.print(completion_panel)

async def main():
    """Run the interactive streaming workflow example."""
    
    console = Console()
    
    # Check if required environment variables are set
    if not os.environ.get("BIGDATA_USERNAME") or not os.environ.get("BIGDATA_PASSWORD"):
        console.print("❌ Error: BIGDATA_USERNAME and BIGDATA_PASSWORD environment variables must be set", style="bold red")
        console.print("Please set them in your environment or .env file", style="yellow")
        return
    
    # Check if Google GenAI API key is set for LLM
    if not os.environ.get("GOOGLE_API_KEY"):
        console.print("❌ Error: GOOGLE_API_KEY environment variable must be set for LLM functionality", style="bold red")
        return
    
    monitor = StreamingProgressMonitor()
    monitor.print_header()
    
    # Define the search topic
    search_topic = "Give me a detailed deep dive on Micron and how demand for memory is expected to change with the pace of AI"
    topic_panel = Panel(
        f"🎯 Research Topic: [bold cyan]{search_topic}[/bold cyan]",
        border_style="blue",
        padding=(0, 1)
    )
    monitor.console.print(topic_panel)
    
    # Set up configuration
    config = {
        "configurable": {
            "search_depth": 2,  # Generate 2 search strategies
            "max_results_per_strategy": 5,  # 5 results per strategy
            "number_of_queries": 2,  # 2 queries per strategy
            "bigdata_rate_limit_delay": 1.5,  # Be conservative with rate limits
            "planner_provider": "google_genai",
            "planner_model": "gemini-2.5-flash",
            "writer_provider": "google_genai", 
            "writer_model": "gemini-2.5-flash",
        }
    }
    
    # Prepare input state
    input_state = {
        "topic": search_topic,
        "search_depth": 2,
        "max_results_per_strategy": 5,
        "entity_preference": None,  # Can provide entity IDs if known
        "date_range": "last_90_days",  # Focus on recent information
    }
    
    # Create configuration table
    config_table = Table(title="⚙️ Workflow Configuration", box=box.ROUNDED)
    config_table.add_column("Setting", style="cyan", no_wrap=True)
    config_table.add_column("Value", style="magenta")
    
    config_table.add_row("Search Strategies", str(config['configurable']['search_depth']))
    config_table.add_row("Results per Strategy", str(config['configurable']['max_results_per_strategy']))
    config_table.add_row("Queries per Strategy", str(config['configurable']['number_of_queries']))
    config_table.add_row("Rate Limit Delay", f"{config['configurable']['bigdata_rate_limit_delay']}s")
    config_table.add_row("Planner Model", f"{config['configurable']['planner_provider']}:{config['configurable']['planner_model']}")
    config_table.add_row("Writer Model", f"{config['configurable']['writer_provider']}:{config['configurable']['writer_model']}")
    
    monitor.console.print(config_table)
    
    try:
        start_panel = Panel(
            "🚀 Starting interactive streaming workflow...\n   Watch real-time progress below!",
            title="🎬 Workflow Starting",
            border_style="bright_blue",
            padding=(1, 2)
        )
        monitor.console.print(start_panel)
        
        # Start the Rich progress bar
        monitor.start_progress()
        
        # Stream the workflow with custom stream mode
        final_result = None
        async for chunk in bigdata_search_graph.astream(
            input_state, 
            config=config,
            stream_mode="custom"  # Use custom stream mode for our rich updates
        ):
            await handle_custom_stream(chunk, monitor)
            
            # Update progress display periodically
            if chunk.get("type") in ["planning_complete", "gathering_complete", "synthesis_complete"]:
                completed_steps = sum(1 for status in monitor.overall_progress.values() if "✅" in status)
                monitor.update_progress(completed_steps)
                monitor.print_status_dashboard()
        
        # Stop the progress bar
        monitor.stop_progress()
        
        # Get the final result using ainvoke to access the complete state
        monitor.console.print("\n📄 Retrieving final research report...", style="bold yellow")
        final_result = await bigdata_search_graph.ainvoke(input_state, config)
        
        if "final_results" in final_result:
            # Use Rich Markdown for beautiful report rendering
            report_markdown = Markdown(final_result["final_results"])
            
            report_panel = Panel(
                report_markdown,
                title="📊 FINAL RESEARCH REPORT",
                border_style="bright_green",
                padding=(1, 2)
            )
            monitor.console.print(report_panel)
        
        # Display final statistics in a beautiful table
        if "source_metadata" in final_result:
            metadata = final_result["source_metadata"]
            
            stats_table = Table(title="📈 Workflow Statistics", box=box.DOUBLE_EDGE)
            stats_table.add_column("Metric", style="cyan", no_wrap=True)
            stats_table.add_column("Value", style="magenta")
            
            stats_table.add_row("Total Searches", str(metadata.get('total_searches', 0)))
            stats_table.add_row("Successful Searches", f"[green]{metadata.get('successful_searches', 0)}[/green]")
            stats_table.add_row("Success Rate", f"{(metadata.get('successful_searches', 0) / max(metadata.get('total_searches', 1), 1) * 100):.1f}%")
            stats_table.add_row("Total Execution Time", f"{metadata.get('total_execution_time', 0):.1f}s")
            stats_table.add_row("Average Time per Search", f"{metadata.get('average_execution_time', 0):.1f}s")
            stats_table.add_row("Total Content Length", f"{metadata.get('total_content_length', 0):,} chars")
            
            # Tool distribution
            tool_dist = metadata.get('tool_type_distribution', {})
            for tool, count in tool_dist.items():
                stats_table.add_row(f"  {tool.capitalize()} Searches", str(count))
                
            monitor.console.print(stats_table)
        
        # Final success message
        total_demo_time = time.time() - monitor.start_time
        success_panel = Panel(
            f"🎉 Interactive streaming workflow completed successfully!\n"
            f"🕐 Total demo time: {total_demo_time:.1f} seconds",
            title="✨ Success",
            border_style="bright_green",
            padding=(1, 2)
        )
        monitor.console.print(success_panel)
        
    except Exception as e:
        error_panel = Panel(
            f"❌ Error executing streaming workflow: {str(e)}\n"
            f"🔧 Error type: {type(e).__name__}\n"
            f"💡 Check your environment variables and network connection",
            title="💥 Workflow Error",
            border_style="red",
            padding=(1, 2)
        )
        monitor.console.print(error_panel)
        
        # Display partial results if available
        if monitor.search_status:
            partial_table = Table(title="📊 Partial Execution Status", box=box.ROUNDED)
            partial_table.add_column("Tool Type", style="yellow", no_wrap=True)
            partial_table.add_column("Status", style="red")
            
            for tool_type, status in monitor.search_status.items():
                partial_table.add_row(tool_type.upper(), status)
                
            monitor.console.print(partial_table)
        
        # Print more detailed error info for debugging
        import traceback
        monitor.console.print("\n🔍 Detailed error traceback:", style="dim red")
        traceback.print_exc()

def run_streaming_example():
    """Synchronous wrapper for the async main function."""
    console = Console()
    
    demo_panel = Panel(
        "🎬 Starting Rich Streaming Demo\n   Press Ctrl+C to interrupt...",
        title="🎭 Demo Starting",
        border_style="bright_cyan",
        padding=(1, 2)
    )
    console.print(demo_panel)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        interrupt_panel = Panel(
            "⏹️ Demo interrupted by user",
            title="🛑 Interrupted",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print(interrupt_panel)
    except Exception as e:
        fatal_panel = Panel(
            f"💥 Fatal error: {str(e)}\n"
            f"💡 Check your setup and try again",
            title="💀 Fatal Error",
            border_style="red",
            padding=(1, 2)
        )
        console.print(fatal_panel)

if __name__ == "__main__":
    run_streaming_example() 