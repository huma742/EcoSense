import re

def fix():
    with open('econosense_app/lib/main.dart', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update _loadUser to extract 'priority'
    load_user_target = """        final Map<String, dynamic> decoded = jsonDecode(actionStr);
        parsedActions.add({
          'title': decoded['title'].toString(),
          'subtitle': decoded['subtitle'].toString(),
          'time': decoded['time'].toString(),
        });"""
    load_user_replace = """        final Map<String, dynamic> decoded = jsonDecode(actionStr);
        parsedActions.add({
          'title': decoded['title'].toString(),
          'subtitle': decoded['subtitle'].toString(),
          'time': decoded['time'].toString(),
          'priority': decoded['priority']?.toString() ?? 'LOW',
        });"""
    content = content.replace(load_user_target, load_user_replace)

    # 2. Update DashboardHome _buildRecentCard call
    recent_target = """              ...recentActions.map((action) => _buildRecentCard(action['title'] ?? '', action['subtitle'] ?? '', action['time'] ?? '')).toList(),"""
    recent_replace = """              ...recentActions.map((action) => _buildRecentCard(action['title'] ?? '', action['subtitle'] ?? '', action['time'] ?? '', action['priority'] ?? 'LOW')).toList(),"""
    content = content.replace(recent_target, recent_replace)

    # 3. Update _buildRecentCard signature and body
    build_card_target = """  Widget _buildRecentCard(String title, String subtitle, String time) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(color: Colors.green.shade50, shape: BoxShape.circle),
          child: const Icon(Icons.article, color: Color(0xFF2E7D32)),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 4.0),
          child: Text(subtitle),
        ),
        trailing: Text(time, style: const TextStyle(fontSize: 12, color: Colors.grey)),
      ),
    );
  }"""
    build_card_replace = """  Widget _buildRecentCard(String title, String subtitle, String time, [String priority = 'LOW']) {
    Color priorityColor;
    switch (priority.toUpperCase()) {
      case 'HIGH': priorityColor = Colors.red; break;
      case 'MED': priorityColor = Colors.orange; break;
      case 'LOW': priorityColor = Colors.blue; break;
      default: priorityColor = Colors.grey;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(color: Colors.green.shade50, shape: BoxShape.circle),
          child: const Icon(Icons.check_circle_outline, color: Color(0xFF2E7D32)),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold), maxLines: 2, overflow: TextOverflow.ellipsis),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 8.0),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Text(subtitle, maxLines: 2, overflow: TextOverflow.ellipsis),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: priorityColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  priority,
                  style: TextStyle(color: priorityColor, fontWeight: FontWeight.bold, fontSize: 10),
                ),
              ),
            ],
          ),
        ),
        trailing: Text(time, style: const TextStyle(fontSize: 12, color: Colors.grey)),
      ),
    );
  }"""
    content = content.replace(build_card_target, build_card_replace)

    # 4. Update newExecution in _executeAction
    content = re.sub(
        r"    final newExecution = \{.*?\};",
        r"    final newExecution = {\n      'title': eventTitle,\n      'subtitle': topAction['description'] ?? 'Action executed successfully.',\n      'time': '${DateTime.now().hour}:${DateTime.now().minute.toString().padLeft(2, '0')}',\n      'priority': topAction['priority'] ?? 'LOW',\n    };",
        content,
        flags=re.DOTALL
    )

    with open('econosense_app/lib/main.dart', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix()
