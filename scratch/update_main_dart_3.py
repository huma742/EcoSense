import os

filepath = r"d:\humaa\EconoSense-pk\econosense_app\lib\main.dart"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update variables in ResultsScreen
old_results_vars = """    final constraints = data['constraints'] ?? {};
    final contradictionAnalysis = data['contradiction_analysis'];
    final temporalAnalysis = data['temporal_analysis'];"""
new_results_vars = """    final constraints = data['constraints'] ?? {};
    final contradictionAnalysis = data['contradiction_analysis'];
    final temporalAnalysis = data['temporal_analysis'];
    final systemAutonomyScore = data['system_autonomy_score'] ?? 100;"""
content = content.replace(old_results_vars, new_results_vars)


# 2. Add Badges to ResultsScreen view
old_results_body = """            if (contradictionAnalysis != null && contradictionAnalysis['contradiction_found'] == true)
              _buildContradictionAlert(contradictionAnalysis),
              
            if (temporalAnalysis != null) ...["""
new_results_body = """            Center(child: _buildAutonomyBadge(systemAutonomyScore)),
            _buildRetryWarnings(agentTrace),

            if (contradictionAnalysis != null && contradictionAnalysis['contradiction_found'] == true)
              _buildContradictionAlert(contradictionAnalysis),
              
            if (temporalAnalysis != null) ...["""
content = content.replace(old_results_body, new_results_body)

# 3. Change "Agent Timeline" section title
old_header = """            _buildSectionHeader('Agent Timeline', Icons.timer),"""
new_header = """            _buildSectionHeader('Antigravity Trace', Icons.terminal),"""
content = content.replace(old_header, new_header)

# 4. Add the Widget methods
new_widgets = """
  Widget _buildAutonomyBadge(int score) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: score == 100 ? Colors.green[50] : Colors.orange[50],
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: score == 100 ? Colors.green[300]! : Colors.orange[300]!),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.smart_toy, color: score == 100 ? Colors.green : Colors.orange, size: 24),
          const SizedBox(width: 8),
          Text('System Autonomy Score: $score%', style: TextStyle(color: score == 100 ? Colors.green[800] : Colors.orange[800], fontWeight: FontWeight.bold, fontSize: 16)),
        ],
      ),
    );
  }

  Widget _buildRetryWarnings(List<Map<String, dynamic>> timeline) {
    final retries = timeline.where((t) => (t['retries'] ?? 0) > 0).toList();
    if (retries.isEmpty) return const SizedBox.shrink();
    
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.yellow[50],
        border: Border.all(color: Colors.yellow[700]!),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: retries.map((r) => Padding(
          padding: const EdgeInsets.only(bottom: 4.0),
          child: Row(
            children: [
              const Icon(Icons.warning_amber_rounded, color: Colors.orange, size: 20),
              const SizedBox(width: 8),
              Expanded(child: Text('⚠️ Agent Retry: ${r['agent']} retried ${r['retries']} times due to API limit', style: const TextStyle(color: Colors.orange, fontWeight: FontWeight.bold))),
            ],
          ),
        )).toList(),
      ),
    );
  }
"""

content = content.replace("  Widget _buildContradictionAlert(Map<String, dynamic> contradiction) {", new_widgets + "\n  Widget _buildContradictionAlert(Map<String, dynamic> contradiction) {")

# 5. Replace _buildTraceCard completely
old_trace_card = """  Widget _buildTraceCard(List<Map<String, dynamic>> agentTrace) {
    return Card(
      elevation: 2,
      color: const Color(0xFF1E1E1E),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: agentTrace.map((trace) {
            if (trace.containsKey('total_time_ms')) {
              return Column(
                children: [
                  const Divider(color: Colors.grey),
                  Padding(
                    padding: const EdgeInsets.only(top: 8.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('TOTAL TIME', style: TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold, fontFamily: 'monospace')),
                        Text('${trace['total_time_ms']} ms', style: const TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold, fontFamily: 'monospace')),
                      ],
                    ),
                  )
                ],
              );
            }
            return Padding(
              padding: const EdgeInsets.only(bottom: 8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Row(
                      children: [
                        Text('> ${trace['agent']}...', style: TextStyle(color: Colors.grey[400], fontFamily: 'monospace', fontSize: 13)),
                        if (trace.containsKey('retries') && trace['retries'] > 0)
                          Padding(
                            padding: const EdgeInsets.only(left: 8.0),
                            child: Container(
                              padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
                              decoration: BoxDecoration(color: Colors.orange.withOpacity(0.2), borderRadius: BorderRadius.circular(4)),
                              child: Text('${trace['retries']} retries', style: const TextStyle(color: Colors.orange, fontSize: 10, fontFamily: 'monospace')),
                            ),
                          )
                      ],
                    ),
                  ),
                  Text('${trace['time_ms']} ms', style: const TextStyle(color: Colors.white, fontFamily: 'monospace', fontSize: 13)),
                ],
              ),
            );
          }).toList(),
        ),
      ),
    );
  }"""

new_trace_card = """  Widget _buildTraceCard(List<Map<String, dynamic>> agentTrace) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1E1E1E), // Dark terminal background
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[800]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.terminal, color: Colors.greenAccent, size: 16),
              SizedBox(width: 8),
              Text('Antigravity System Orchestrator', style: TextStyle(color: Colors.greenAccent, fontFamily: 'monospace', fontWeight: FontWeight.bold, fontSize: 14)),
            ],
          ),
          const Divider(color: Colors.grey),
          ...agentTrace.map((trace) {
            if (trace.containsKey('total_time_ms')) {
              return Padding(
                padding: const EdgeInsets.only(top: 12.0),
                child: Text('> Execution finished in ${trace['total_time_ms']}ms', style: const TextStyle(color: Colors.yellow, fontFamily: 'monospace', fontWeight: FontWeight.bold)),
              );
            }
            
            final reasoningList = List<String>.from(trace['reasoning_trace'] ?? []);
            return Padding(
              padding: const EdgeInsets.only(bottom: 16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('[${trace['agent']}]', style: const TextStyle(color: Colors.cyanAccent, fontFamily: 'monospace', fontWeight: FontWeight.bold)),
                      Text('${trace['time_ms']}ms', style: const TextStyle(color: Colors.grey, fontFamily: 'monospace', fontSize: 12)),
                    ],
                  ),
                  const SizedBox(height: 4),
                  ...reasoningList.map((step) => Padding(
                    padding: const EdgeInsets.only(left: 12.0, bottom: 2.0),
                    child: Text('  $step', style: TextStyle(color: Colors.green[300], fontFamily: 'monospace', fontSize: 12)),
                  )).toList(),
                  if ((trace['retries'] ?? 0) > 0)
                    Padding(
                      padding: const EdgeInsets.only(left: 12.0, top: 4.0),
                      child: Text('  [WARN] Retries used: ${trace['retries']}', style: const TextStyle(color: Colors.orange, fontFamily: 'monospace', fontSize: 12, fontWeight: FontWeight.bold)),
                    ),
                ],
              ),
            );
          }).toList(),
        ],
      ),
    );
  }"""
content = content.replace(old_trace_card, new_trace_card)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Dart file updated successfully.")
