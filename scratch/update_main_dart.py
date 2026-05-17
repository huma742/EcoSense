import os

filepath = r"d:\humaa\EconoSense-pk\econosense_app\lib\main.dart"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update TabController length
content = content.replace(
    "_tabController = TabController(length: 3, vsync: this);",
    "_tabController = TabController(length: 4, vsync: this);"
)

# 2. Update Tabs
old_tabs = """          tabs: const [
            Tab(icon: Icon(Icons.text_fields), text: 'Text'),
            Tab(icon: Icon(Icons.link), text: 'URL'),
            Tab(icon: Icon(Icons.picture_as_pdf), text: 'PDF'),
          ],"""
new_tabs = """          tabs: const [
            Tab(icon: Icon(Icons.text_fields), text: 'Text'),
            Tab(icon: Icon(Icons.link), text: 'URL'),
            Tab(icon: Icon(Icons.picture_as_pdf), text: 'PDF'),
            Tab(icon: Icon(Icons.library_books), text: 'Multi-Source'),
          ],"""
content = content.replace(old_tabs, new_tabs)

# 3. Update TabBarView children
old_tab_children = """      body: TabBarView(
        controller: _tabController,
        children: [
          _buildTextTab(),
          _buildUrlTab(),
          _buildPdfTab(),
        ],
      ),"""
new_tab_children = """      body: TabBarView(
        controller: _tabController,
        children: [
          _buildTextTab(),
          _buildUrlTab(),
          _buildPdfTab(),
          _buildMultiSourceTab(),
        ],
      ),"""
content = content.replace(old_tab_children, new_tab_children)

# 4. Add new controllers and Multi-Source functions
old_controllers = """  final TextEditingController _urlController = TextEditingController();
  bool _isLoading = false;"""
new_controllers = """  final TextEditingController _urlController = TextEditingController();
  final TextEditingController _source1Controller = TextEditingController();
  final TextEditingController _source2Controller = TextEditingController();
  final TextEditingController _source3Controller = TextEditingController();
  bool _isLoading = false;"""
content = content.replace(old_controllers, new_controllers)

old_dispose = """    _tabController.dispose();
    _textController.dispose();
    _urlController.dispose();
    super.dispose();"""
new_dispose = """    _tabController.dispose();
    _textController.dispose();
    _urlController.dispose();
    _source1Controller.dispose();
    _source2Controller.dispose();
    _source3Controller.dispose();
    super.dispose();"""
content = content.replace(old_dispose, new_dispose)

multi_source_code = """
  // --- 5. Multi-Source ---
  Future<void> _analyzeMulti() async {
    final s1 = _source1Controller.text.trim();
    final s2 = _source2Controller.text.trim();
    final s3 = _source3Controller.text.trim();
    
    final sources = [s1, s2, s3].where((s) => s.isNotEmpty).toList();
    if (sources.length < 2) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Please enter at least 2 sources')));
      return;
    }

    setState(() => _isLoading = true);
    try {
      final uri = Uri.parse('http://192.168.100.20:8000/analyze-multi');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'sources': sources}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (!mounted) return;
        Navigator.push(context, MaterialPageRoute(builder: (_) => ResultsScreen(data: data)));
      } else {
        throw Exception('Server Error: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Multi-Source Error: $e'), backgroundColor: Colors.red));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Widget _buildMultiSourceTab() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const SizedBox(height: 16),
                  const Text('Analyze multiple sources for contradictions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 16),
                  TextField(controller: _source1Controller, maxLines: 4, decoration: const InputDecoration(hintText: 'Source 1 text...')),
                  const SizedBox(height: 12),
                  TextField(controller: _source2Controller, maxLines: 4, decoration: const InputDecoration(hintText: 'Source 2 text...')),
                  const SizedBox(height: 12),
                  TextField(controller: _source3Controller, maxLines: 4, decoration: const InputDecoration(hintText: 'Source 3 text (optional)...')),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          _buildAnalyzeButton('Analyze Multiple Sources', _analyzeMulti),
        ],
      ),
    );
  }
"""

# Insert multi_source_code before "Widget _buildAnalyzeButton"
content = content.replace("  Widget _buildAnalyzeButton(String label, VoidCallback onPressed) {", multi_source_code + "\n  Widget _buildAnalyzeButton(String label, VoidCallback onPressed) {")

# 5. Update ResultsScreen build method
old_results_vars = """    final insights = data['insights'] ?? {};
    final actions = List<Map<String, dynamic>>.from(data['actions'] ?? []);
    final simulation = data['simulation'] ?? {};
    final agentTrace = List<Map<String, dynamic>>.from(data['agent_trace'] ?? []);"""
new_results_vars = """    final insights = data['insights'] ?? {};
    final actions = List<Map<String, dynamic>>.from(data['actions'] ?? []);
    final simulation = data['simulation'] ?? {};
    final agentTrace = List<Map<String, dynamic>>.from(data['agent_timeline'] ?? data['agent_trace'] ?? []);
    final actionChain = List<Map<String, dynamic>>.from(data['action_chain'] ?? []);
    final constraints = data['constraints'] ?? {};
    final contradictionAnalysis = data['contradiction_analysis'];"""
content = content.replace(old_results_vars, new_results_vars)


old_results_body = """            _buildSectionHeader('Event Insights', Icons.auto_graph),
            _buildInsightsCard(insights, riskScore),
            
            const SizedBox(height: 24),"""
new_results_body = """            if (contradictionAnalysis != null && contradictionAnalysis['contradiction_found'] == true)
              _buildContradictionAlert(contradictionAnalysis),
            
            _buildSectionHeader('Event Insights', Icons.auto_graph),
            _buildInsightsCard(insights, riskScore),
            
            const SizedBox(height: 24),"""
content = content.replace(old_results_body, new_results_body)

old_results_actions = """            const SizedBox(height: 24),
            _buildSectionHeader('Simulation (Top Action)', Icons.science),"""
new_results_actions = """            if (actionChain.isNotEmpty) ...[
              const SizedBox(height: 24),
              _buildSectionHeader('Action Chain', Icons.linear_scale),
              ActionChainAnimatedViewer(actionChain: actionChain),
            ],

            if (constraints.isNotEmpty) ...[
              const SizedBox(height: 24),
              _buildSectionHeader('Constraint Check', Icons.gavel),
              _buildConstraintCard(constraints),
            ],

            const SizedBox(height: 24),
            _buildSectionHeader('Simulation (Top Action)', Icons.science),"""
content = content.replace(old_results_actions, new_results_actions)

# 6. Add new widgets to ResultsScreen
new_widgets = """
  Widget _buildContradictionAlert(Map<String, dynamic> contradiction) {
    final claims = List<String>.from(contradiction['conflicting_claims'] ?? []);
    return Container(
      margin: const EdgeInsets.only(bottom: 24),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.red[50],
        border: Border.all(color: Colors.red[300]!),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: const [
              Icon(Icons.warning_amber_rounded, color: Colors.red, size: 28),
              SizedBox(width: 8),
              Text('⚠️ Contradiction Detected!', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold, fontSize: 18)),
            ],
          ),
          const SizedBox(height: 12),
          const Text('Conflicting Claims:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.red)),
          const SizedBox(height: 4),
          ...claims.map((c) => Padding(
            padding: const EdgeInsets.only(bottom: 4),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('• ', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)),
                Expanded(child: Text(c, style: const TextStyle(fontSize: 14))),
              ],
            ),
          )).toList(),
          const SizedBox(height: 12),
          const Text('Resolution:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.red)),
          const SizedBox(height: 4),
          Text(contradiction['resolution'] ?? '', style: const TextStyle(fontSize: 14)),
        ],
      ),
    );
  }

  Widget _buildConstraintCard(Map<String, dynamic> constraints) {
    final isFeasible = constraints['feasible'] == true;
    final color = isFeasible ? Colors.green : Colors.red;
    
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16), side: BorderSide(color: color.withOpacity(0.5))),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(isFeasible ? Icons.check_circle : Icons.cancel, color: color, size: 28),
                const SizedBox(width: 12),
                Text(isFeasible ? 'FEASIBLE' : 'INFEASIBLE', style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 18)),
              ],
            ),
            const Divider(height: 24),
            Text('Reason', style: TextStyle(color: Colors.grey[600], fontSize: 12, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(constraints['reason'] ?? 'N/A', style: const TextStyle(fontSize: 14)),
            const SizedBox(height: 16),
            Text('Adjustments Needed', style: TextStyle(color: Colors.grey[600], fontSize: 12, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(constraints['adjustments_needed'] ?? 'None', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
          ],
        ),
      ),
    );
  }
"""
content = content.replace("  Widget _buildTraceCard(List<Map<String, dynamic>> agentTrace) {", new_widgets + "  Widget _buildTraceCard(List<Map<String, dynamic>> agentTrace) {")

action_chain_class = """
class ActionChainAnimatedViewer extends StatefulWidget {
  final List<Map<String, dynamic>> actionChain;
  const ActionChainAnimatedViewer({super.key, required this.actionChain});

  @override
  State<ActionChainAnimatedViewer> createState() => _ActionChainAnimatedViewerState();
}

class _ActionChainAnimatedViewerState extends State<ActionChainAnimatedViewer> {
  int _currentVisibleIndex = 0;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _startAnimation();
  }

  void _startAnimation() {
    _timer = Timer.periodic(const Duration(milliseconds: 800), (timer) {
      if (_currentVisibleIndex < widget.actionChain.length) {
        if (mounted) {
          setState(() {
            _currentVisibleIndex++;
          });
        }
      } else {
        timer.cancel();
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: List.generate(widget.actionChain.length, (index) {
        final step = widget.actionChain[index];
        final bool isVisible = index < _currentVisibleIndex;
        
        return AnimatedOpacity(
          opacity: isVisible ? 1.0 : 0.0,
          duration: const Duration(milliseconds: 500),
          child: AnimatedSlide(
            offset: isVisible ? Offset.zero : const Offset(0, 0.2),
            duration: const Duration(milliseconds: 500),
            child: _buildChainStep(step, index),
          ),
        );
      }),
    );
  }

  Widget _buildChainStep(Map<String, dynamic> step, int index) {
    final status = step['status'] ?? 'pending';
    Color statusColor;
    IconData statusIcon;
    switch(status.toString().toLowerCase()) {
      case 'completed': statusColor = Colors.green; statusIcon = Icons.check_circle; break;
      case 'executing': statusColor = Colors.orange; statusIcon = Icons.run_circle; break;
      default: statusColor = Colors.grey; statusIcon = Icons.pending;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: statusColor.withOpacity(0.2),
          child: Text('${step['step_number'] ?? index + 1}', style: TextStyle(color: statusColor, fontWeight: FontWeight.bold)),
        ),
        title: Text(step['action'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 8.0),
          child: Text('Result: ${step['result'] ?? ''}', style: TextStyle(color: Colors.grey[700], fontSize: 13)),
        ),
        trailing: Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
          decoration: BoxDecoration(color: statusColor.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(statusIcon, color: statusColor, size: 16),
              const SizedBox(width: 4),
              Text(status.toString().toUpperCase(), style: TextStyle(color: statusColor, fontSize: 10, fontWeight: FontWeight.bold)),
            ],
          ),
        ),
      ),
    );
  }
}
"""
content = content + "\n" + action_chain_class

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Dart file updated successfully.")
