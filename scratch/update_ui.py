import re

def update_ui():
    with open('econosense_app/lib/main.dart', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update DashboardScreen State
    ds_state_target = """  String _userEmail = 'analyst@econosense.pk';

  @override"""
    ds_state_replace = """  String _userEmail = 'analyst@econosense.pk';
  List<Map<String, String>> _recentActions = [];

  @override"""
    content = content.replace(ds_state_target, ds_state_replace)

    # 2. Update _loadUser in DashboardScreen
    load_user_target = """  Future<void> _loadUser() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _userName = prefs.getString('name') ?? 'Analyst';
      _userEmail = prefs.getString('email') ?? 'analyst@econosense.pk';
    });
  }"""
    load_user_replace = """  Future<void> _loadUser() async {
    final prefs = await SharedPreferences.getInstance();
    final savedActions = prefs.getStringList('executed_actions') ?? [];
    
    List<Map<String, String>> parsedActions = [];
    for (var actionStr in savedActions) {
      try {
        final Map<String, dynamic> decoded = jsonDecode(actionStr);
        parsedActions.add({
          'title': decoded['title'].toString(),
          'subtitle': decoded['subtitle'].toString(),
          'time': decoded['time'].toString(),
        });
      } catch(e) {}
    }
    
    setState(() {
      _userName = prefs.getString('name') ?? 'Analyst';
      _userEmail = prefs.getString('email') ?? 'analyst@econosense.pk';
      _recentActions = parsedActions.reversed.toList(); // Newest first
    });
  }"""
    content = content.replace(load_user_target, load_user_replace)

    # 3. Update DashboardScreen screens array
    screens_target = """      DashboardHome(userName: _userName, onLogout: _logout),"""
    screens_replace = """      DashboardHome(userName: _userName, onLogout: _logout, recentActions: _recentActions),"""
    content = content.replace(screens_target, screens_replace)

    # 4. Update DashboardHome constructor and fields
    dh_target = """class DashboardHome extends StatelessWidget {
  final String userName;
  final VoidCallback onLogout;

  const DashboardHome({super.key, required this.userName, required this.onLogout});"""
    dh_replace = """class DashboardHome extends StatelessWidget {
  final String userName;
  final VoidCallback onLogout;
  final List<Map<String, String>> recentActions;

  const DashboardHome({super.key, required this.userName, required this.onLogout, this.recentActions = const []});"""
    content = content.replace(dh_target, dh_replace)

    # 5. Update DashboardHome recent analyses section
    recent_target = """            const SizedBox(height: 32),
            const Text('Recent Analyses', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildRecentCard('IMF Bailout Package Approved', 'High Risk • Energy Sector', '2 hours ago'),
            _buildRecentCard('IT Exports Cross \$3 Billion', 'Low Risk • Tech Sector', 'Yesterday'),
            _buildRecentCard('SBP Keeps Interest Rate at 22%', 'Medium Risk • Finance', '2 days ago'),"""
    recent_replace = """            const SizedBox(height: 32),
            const Text('Recent Executed Actions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            if (recentActions.isEmpty)
              _buildRecentCard('No actions executed yet', 'Run analysis and execute an action', 'Now')
            else
              ...recentActions.map((action) => _buildRecentCard(action['title'] ?? '', action['subtitle'] ?? '', action['time'] ?? '')).toList(),"""
    content = content.replace(recent_target, recent_replace)

    # 6. ResultsScreen _buildActionCard signature and body
    action_card_target = """  Widget _buildActionCard(Map<String, dynamic> action) {
    final priority = action['priority'] ?? 'LOW';
    final color = _getPriorityColor(priority);
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: color.withOpacity(0.3), width: 1),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                priority,
                style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12),
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                action['description'] ?? 'N/A',
                style: const TextStyle(fontSize: 15, height: 1.4),
              ),
            ),
          ],
        ),
      ),
    );
  }"""
    action_card_replace = """  Widget _buildActionCard(Map<String, dynamic> action) {
    final priority = action['priority'] ?? 'LOW';
    final color = _getPriorityColor(priority);
    final target = action['target'] ?? 'N/A';
    final timeline = action['timeline'] ?? 'N/A';
    final expectedOutcome = action['expected_outcome'] ?? 'N/A';
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: color.withOpacity(0.3), width: 1),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    priority,
                    style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Text(
                    action['description'] ?? 'N/A',
                    style: const TextStyle(fontSize: 15, height: 1.4, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const Padding(padding: EdgeInsets.symmetric(vertical: 8), child: Divider()),
            Row(
              children: [
                const Icon(Icons.person, size: 16, color: Colors.green),
                const SizedBox(width: 8),
                Expanded(child: Text('Target: $target', style: const TextStyle(fontSize: 13, color: Colors.black87))),
              ],
            ),
            const SizedBox(height: 6),
            Row(
              children: [
                const Icon(Icons.access_time, size: 16, color: Colors.orange),
                const SizedBox(width: 8),
                Expanded(child: Text('Timeline: $timeline', style: const TextStyle(fontSize: 13, color: Colors.black87))),
              ],
            ),
            const SizedBox(height: 6),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.check_circle, size: 16, color: Colors.blue),
                const SizedBox(width: 8),
                Expanded(child: Text('Outcome: $expectedOutcome', style: const TextStyle(fontSize: 13, color: Colors.black87))),
              ],
            ),
          ],
        ),
      ),
    );
  }"""
    content = content.replace(action_card_target, action_card_replace)

    # 7. Update _buildInsightsCard to show new fields
    insights_card_target = """            const Divider(height: 32),
            Text('Impact Summary', style: TextStyle(color: Colors.grey[600], fontSize: 12, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(insights['impact_summary'] ?? 'N/A', style: const TextStyle(fontSize: 14, height: 1.5)),
          ],
        ),"""
    insights_card_replace = """            const Divider(height: 32),
            Text('Impact Summary', style: TextStyle(color: Colors.grey[600], fontSize: 12, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(insights['impact_summary'] ?? 'N/A', style: const TextStyle(fontSize: 14, height: 1.5)),
            const SizedBox(height: 16),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.warning_amber_rounded, size: 20, color: Colors.orange),
                const SizedBox(width: 8),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Why It Matters', style: TextStyle(color: Colors.grey[600], fontSize: 12, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 4),
                      Text(insights['why_it_matters'] ?? 'N/A', style: const TextStyle(fontSize: 14)),
                    ],
                  )
                )
              ]
            ),
            const SizedBox(height: 16),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.people, size: 20, color: Colors.blue),
                const SizedBox(width: 8),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Affected Population', style: TextStyle(color: Colors.grey[600], fontSize: 12, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 4),
                      Text(insights['affected_population'] ?? 'N/A', style: const TextStyle(fontSize: 14)),
                    ],
                  )
                )
              ]
            ),
          ],
        ),"""
    content = content.replace(insights_card_target, insights_card_replace)

    # 8. Add "Execute Top Action" logic and button in ResultsScreen
    execute_button_code = """
            const SizedBox(height: 16),
            if (actions.isNotEmpty)
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () => _executeAction(context, actions[0], insights['event'] ?? 'Analysis'),
                  icon: const Icon(Icons.play_arrow),
                  label: const Text('Execute Top Action', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF2E7D32),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                ),
              ),"""
              
    actions_list_target = """            ...actions.map((action) => _buildActionCard(action)).toList(),"""
    actions_list_replace = """            ...actions.map((action) => _buildActionCard(action)).toList(),""" + execute_button_code
    content = content.replace(actions_list_target, actions_list_replace)

    # 9. Add _executeAction method to ResultsScreen
    execute_method = """
  Future<void> _executeAction(BuildContext context, Map<String, dynamic> topAction, String eventTitle) async {
    // Show executing dialog
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        content: Row(
          children: const [
            CircularProgressIndicator(color: Color(0xFF2E7D32)),
            SizedBox(width: 24),
            Text('Executing Action...', style: TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );

    // Wait 3 seconds
    await Future.delayed(const Duration(seconds: 3));
    
    // Pop loading dialog
    if (context.mounted) Navigator.pop(context);

    // Save to SharedPreferences
    final prefs = await SharedPreferences.getInstance();
    List<String> savedActions = prefs.getStringList('executed_actions') ?? [];
    
    final newExecution = {
      'title': 'Executed: ${topAction['priority'] ?? 'Action'}',
      'subtitle': topAction['description'] ?? 'Action executed successfully.',
      'time': '${DateTime.now().hour}:${DateTime.now().minute.toString().padLeft(2, '0')}',
      'event': eventTitle,
    };
    
    savedActions.add(jsonEncode(newExecution));
    await prefs.setStringList('executed_actions', savedActions);

    // Show success dialog
    if (context.mounted) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: Row(
            children: const [
              Icon(Icons.check_circle, color: Colors.green),
              SizedBox(width: 8),
              Text('Success'),
            ],
          ),
          content: const Text('Action Executed Successfully! Saved to Dashboard.'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context); // Close dialog
              },
              child: const Text('OK', style: TextStyle(color: Color(0xFF2E7D32))),
            )
          ],
        ),
      );
    }
  }

  @override"""
    
    content = content.replace("  @override\n  Widget build(BuildContext context) {", execute_method + "\n  Widget build(BuildContext context) {")

    with open('econosense_app/lib/main.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("UI Update Complete")

if __name__ == '__main__':
    update_ui()
