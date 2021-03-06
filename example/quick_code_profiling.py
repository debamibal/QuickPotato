from example.example_code import FancyCode
from QuickPotato.configuration.management import options
from QuickPotato.statistical.visualizations import FlameGraph, CsvFile


options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled

FancyCode().say_my_name_and_more(name="joey hendricks")

# Generate Flame Graph
FlameGraph().export("C:\\temp\\")
CsvFile().export("C:\\temp\\")
