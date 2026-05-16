import re

def fix():
    with open('econosense_app/lib/main.dart', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove _executeAction from SplashScreen
    first_execute = content.find("  Future<void> _executeAction(BuildContext context")
    if first_execute != -1:
        first_build = content.find("  @override\n  Widget build(BuildContext context)", first_execute)
        
        execute_code = content[first_execute:first_build]
        # Remove it from the current location
        content = content[:first_execute] + content[first_build:]
        
        # 2. Insert it into ResultsScreen right before its build method.
        results_screen_idx = content.find('class ResultsScreen extends StatelessWidget {')
        results_build_idx = content.find("  @override\n  Widget build(BuildContext context)", results_screen_idx)
        
        content = content[:results_build_idx] + execute_code + content[results_build_idx:]
        
    # 3. Update the OK button to double pop and fix Dashboard tab onTap
    dialog_target = """            TextButton(
              onPressed: () {
                Navigator.pop(context); // Close dialog
              },
              child: const Text('OK', style: TextStyle(color: Color(0xFF2E7D32))),"""
    dialog_replace = """            TextButton(
              onPressed: () {
                Navigator.pop(context); // Close dialog
                Navigator.pop(context); // Pop ResultsScreen
              },
              child: const Text('OK', style: TextStyle(color: Color(0xFF2E7D32))),"""
    content = content.replace(dialog_target, dialog_replace)
    
    ontap_target = """        onTap: (index) => setState(() => _currentIndex = index),"""
    ontap_replace = """        onTap: (index) {
          setState(() => _currentIndex = index);
          if (index == 0) _loadUser();
        },"""
    content = content.replace(ontap_target, ontap_replace)

    with open('econosense_app/lib/main.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('Fixed')

if __name__ == '__main__':
    fix()
