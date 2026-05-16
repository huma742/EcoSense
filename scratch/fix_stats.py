import re

def fix():
    with open('econosense_app/lib/main.dart', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix old dashboard items by preferring 'event' key over 'title'
    load_user_target = """        parsedActions.add({
          'title': decoded['title'].toString(),
          'subtitle': decoded['subtitle'].toString(),
          'time': decoded['time'].toString(),
          'priority': decoded['priority']?.toString() ?? 'LOW',
        });"""
    load_user_replace = """        parsedActions.add({
          'title': (decoded['event'] ?? decoded['title']).toString(),
          'subtitle': decoded['subtitle'].toString(),
          'time': decoded['time'].toString(),
          'priority': decoded['priority']?.toString() ?? 'LOW',
        });"""
    content = content.replace(load_user_target, load_user_replace)

    # 2. Update DashboardHome Stats Cards
    stats_target = """            Row(
              children: [
                Expanded(child: _buildStatCard('Analyses', '12', Icons.insert_chart, Colors.blue)),
                const SizedBox(width: 16),
                Expanded(child: _buildStatCard('Avg Risk', '6.5', Icons.warning, Colors.orange)),
              ],
            ),"""
    stats_replace = """            Row(
              children: [
                Expanded(child: _buildStatCard('Actions Executed', '${recentActions.length}', Icons.insert_chart, Colors.blue)),
              ],
            ),"""
    content = content.replace(stats_target, stats_replace)

    with open('econosense_app/lib/main.dart', 'w', encoding='utf-8') as f:
        f.write(content)
        
if __name__ == '__main__':
    fix()
