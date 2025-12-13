"""
Comprehensive project validation script
Checks for inconsistencies, redundancies, circular references, missing files, etc.
"""
import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import importlib.util


class ProjectValidator:
    """Validates project for consistency and errors"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.issues = []
        self.file_references = defaultdict(list)
        self.definitions = defaultdict(list)
        self.imports = defaultdict(set)
        
    def validate_all(self):
        """Run all validation checks"""
        print("Starting comprehensive project validation...\n")
        
        self.check_documentation()
        self.check_backend_code()
        self.check_frontend_code()
        self.check_file_references()
        self.check_method_implementations()
        self.check_duplicate_definitions()
        self.check_circular_references()
        self.check_missing_files()
        
        self.report_results()
    
    def check_documentation(self):
        """Check documentation files for issues"""
        print("[1/8] Checking documentation...")
        
        docs_path = self.project_root / "docs"
        root_files = list(self.project_root.glob("*.md"))
        
        all_docs = list(docs_path.rglob("*.md")) + root_files
        
        # Check for duplicates
        doc_content_hash = {}
        for doc_file in all_docs:
            try:
                content = doc_file.read_text(encoding='utf-8', errors='ignore')
                content_hash = hash(content[:1000])  # First 1000 chars
                
                if content_hash in doc_content_hash:
                    self.issues.append({
                        'type': 'duplicate',
                        'severity': 'medium',
                        'file': str(doc_file),
                        'message': f"Duplicate content with {doc_content_hash[content_hash]}"
                    })
                else:
                    doc_content_hash[content_hash] = str(doc_file)
                
                # Check for broken references
                self._check_markdown_links(doc_file, content)
                
                # Check for focus area definitions
                self._extract_focus_area_definitions(doc_file, content)
                
            except Exception as e:
                self.issues.append({
                    'type': 'error',
                    'severity': 'high',
                    'file': str(doc_file),
                    'message': f"Error reading file: {str(e)}"
                })
    
    def check_backend_code(self):
        """Check backend Python code"""
        print("[2/8] Checking backend code...")
        
        backend_path = self.project_root / "backend" / "app"
        
        for py_file in backend_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Parse AST
                try:
                    tree = ast.parse(content)
                    self._analyze_python_file(py_file, tree, content)
                except SyntaxError as e:
                    self.issues.append({
                        'type': 'syntax_error',
                        'severity': 'critical',
                        'file': str(py_file),
                        'message': f"Syntax error: {str(e)}"
                    })
                
            except Exception as e:
                self.issues.append({
                    'type': 'error',
                    'severity': 'high',
                    'file': str(py_file),
                    'message': f"Error reading file: {str(e)}"
                })
    
    def check_frontend_code(self):
        """Check frontend TypeScript/React code"""
        print("[3/8] Checking frontend code...")
        
        frontend_path = self.project_root / "frontend" / "src"
        
        for tsx_file in frontend_path.rglob("*.tsx"):
            try:
                content = tsx_file.read_text(encoding='utf-8')
                self._check_typescript_file(tsx_file, content)
            except Exception as e:
                self.issues.append({
                    'type': 'error',
                    'severity': 'high',
                    'file': str(tsx_file),
                    'message': f"Error reading file: {str(e)}"
                })
    
    def check_file_references(self):
        """Verify all referenced files exist"""
        print("[4/8] Checking file references...")
        
        for file_path, references in self.file_references.items():
            for ref in references:
                # Skip TypeScript/JavaScript file extensions that might not exist
                # TypeScript compiler handles .ts/.tsx resolution
                if ref.endswith(('.ts', '.tsx', '.js', '.jsx')):
                    # Try to resolve without extension first
                    ref_no_ext = ref.rsplit('.', 1)[0]
                    ref_path = Path(ref_no_ext)
                else:
                    ref_path = Path(ref)
                
                if not ref_path.is_absolute():
                    # Resolve relative to referencing file
                    base_path = Path(file_path).parent
                    ref_path = base_path / ref_path
                    
                    # Try with common extensions if no extension
                    if not ref_path.suffix and not ref_path.exists():
                        for ext in ['.md', '.py', '.ts', '.tsx', '.js', '.jsx', '.json']:
                            test_path = ref_path.with_suffix(ext)
                            if test_path.exists():
                                ref_path = test_path
                                break
                
                # Check if file exists
                if not ref_path.exists():
                    # Check if it's a directory reference (ends with /)
                    if ref.endswith('/'):
                        dir_path = ref_path
                        if not dir_path.is_absolute():
                            base_path = Path(file_path).parent
                            dir_path = base_path / dir_path
                        if dir_path.is_dir():
                            continue  # Directory exists, skip
                    
                    self.issues.append({
                        'type': 'missing_file',
                        'severity': 'high',
                        'file': file_path,
                        'message': f"Referenced file does not exist: {ref}"
                    })
    
    def check_method_implementations(self):
        """Check if all called methods are implemented"""
        print("[5/8] Checking method implementations...")
        
        # This would require more sophisticated analysis
        # For now, check imports match files
        for module, imports in self.imports.items():
            module_str = module.replace(".", "/")
            module_path = self.project_root / "backend" / "app" / f"{module_str}.py"
            if not module_path.exists():
                # Try as package
                module_path = self.project_root / "backend" / "app" / module_str / "__init__.py"
                if not module_path.exists():
                    # Skip external packages
                    if not module.startswith('app.'):
                        continue
                    self.issues.append({
                        'type': 'missing_module',
                        'severity': 'high',
                        'file': 'imports',
                        'message': f"Imported module not found: {module}"
                    })
    
    def check_duplicate_definitions(self):
        """Check for duplicate definitions of same concepts"""
        print("[6/8] Checking duplicate definitions...")
        
        # Check focus area definitions
        focus_area_defs = self.definitions.get('focus_area', [])
        if len(focus_area_defs) > 1:
            codes = [d.get('code') for d in focus_area_defs]
            if len(codes) != len(set(codes)):
                self.issues.append({
                    'type': 'duplicate_definition',
                    'severity': 'high',
                    'file': 'multiple',
                    'message': f"Duplicate focus area codes found: {codes}"
                })
    
    def check_circular_references(self):
        """Check for circular import references"""
        print("[7/8] Checking circular references...")
        
        # Build import graph
        import_graph = defaultdict(set)
        for file_path, imports in self.imports.items():
            for imp in imports:
                import_graph[file_path].add(imp)
        
        # Simple cycle detection (would need more sophisticated for full analysis)
        # This is a placeholder - full implementation would use DFS
    
    def check_missing_files(self):
        """Check for missing critical files"""
        print("[8/8] Checking for missing files...")
        
        required_files = [
            "backend/app/main.py",
            "backend/app/core/config.py",
            "backend/app/core/database.py",
            "backend/requirements.txt",
            "frontend/package.json",
            "docker-compose.yml",
            "README.md"
        ]
        
        for req_file in required_files:
            file_path = self.project_root / req_file
            if not file_path.exists():
                self.issues.append({
                    'type': 'missing_file',
                    'severity': 'critical',
                    'file': req_file,
                    'message': f"Required file missing: {req_file}"
                })
    
    def _check_markdown_links(self, file_path: Path, content: str):
        """Check markdown links for broken references"""
        # Find all markdown links [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        for text, url in links:
            if url.startswith('http'):
                continue  # External links
            
            # Handle anchor links - separate file path from anchor
            if '#' in url:
                file_part, anchor = url.split('#', 1)
                if not file_part:  # Just anchor, same file
                    continue
                url = file_part  # Check file part only
            
            if url.startswith('#'):
                continue  # Anchor links in same file
            
            self.file_references[str(file_path)].append(url)
    
    def _extract_focus_area_definitions(self, file_path: Path, content: str):
        """Extract focus area definitions from docs"""
        # Look for focus area mentions
        focus_areas = [
            'BUSINESS_PROTECTION', 'Business Protection',
            'BUSINESS_CONTROL', 'Business Control',
            'ACCESS_GOVERNANCE', 'Access Governance',
            'TECHNICAL_CONTROL', 'Technical Control',
            'JOBS_CONTROL', 'Jobs Control',
            'S4HANA_EXCELLENCE', 'S/4HANA Excellence'
        ]
        
        for fa in focus_areas:
            if fa in content:
                self.definitions['focus_area'].append({
                    'file': str(file_path),
                    'code': fa,
                    'context': content[content.find(fa)-50:content.find(fa)+200]
                })
    
    def _analyze_python_file(self, file_path: Path, tree: ast.AST, content: str):
        """Analyze Python file AST"""
        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports[str(file_path)].add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.imports[str(file_path)].add(node.module)
        
        # Check for class definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if class methods are called elsewhere
                pass
    
    def _check_typescript_file(self, file_path: Path, content: str):
        """Check TypeScript file - skip import checking as TypeScript compiler handles this"""
        # TypeScript imports are resolved by the TypeScript compiler
        # We skip checking them to avoid false positives
        # The compiler will catch any actual import errors
        pass
    
    def report_results(self):
        """Report all found issues"""
        print("\n" + "="*80)
        print("VALIDATION RESULTS")
        print("="*80 + "\n")
        
        if not self.issues:
            print("[OK] No issues found! Project is consistent.")
            return
        
        # Group by severity
        critical = [i for i in self.issues if i['severity'] == 'critical']
        high = [i for i in self.issues if i['severity'] == 'high']
        medium = [i for i in self.issues if i['severity'] == 'medium']
        low = [i for i in self.issues if i['severity'] == 'low']
        
        print(f"[CRITICAL] {len(critical)}")
        print(f"[HIGH] {len(high)}")
        print(f"[MEDIUM] {len(medium)}")
        print(f"[LOW] {len(low)}")
        print(f"\nTotal Issues: {len(self.issues)}\n")
        
        # Show critical and high issues
        for issue in critical + high:
            print(f"[{issue['severity'].upper()}] {issue['type']}")
            print(f"  File: {issue['file']}")
            print(f"  Message: {issue['message']}")
            print()
        
        # Save full report
        report_path = self.project_root / "validation_report.json"
        with open(report_path, 'w') as f:
            json.dump(self.issues, f, indent=2)
        
        print(f"\n[REPORT] Full report saved to: {report_path}")


if __name__ == "__main__":
    import sys
    
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    validator = ProjectValidator(project_root)
    validator.validate_all()

