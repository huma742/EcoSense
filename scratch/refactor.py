import re

def refactor():
    with open('econosense_app/lib/main.dart', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update SplashScreen
    splash_target = """    final prefs = await SharedPreferences.getInstance();
    final bool isLoggedIn = prefs.getBool('isLoggedIn') ?? false;

    if (mounted) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => isLoggedIn ? const DashboardScreen() : const LoginScreen()),
      );
    }"""
    splash_replace = """    if (mounted) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const DashboardScreen()),
      );
    }"""
    content = content.replace(splash_target, splash_replace)

    # 2. Update _logout
    logout_target = """  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isLoggedIn', false);
    if (mounted) {
      Navigator.pushAndRemoveUntil(context, MaterialPageRoute(builder: (_) => const LoginScreen()), (route) => false);
    }
  }"""
    logout_replace = """  Future<void> _logout() async {
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Logout disabled in this version')));
  }"""
    content = content.replace(logout_target, logout_replace)

    # 3. Remove LoginScreen and SignupScreen classes
    start_idx = content.find('// 2. LOGIN SCREEN')
    end_idx = content.find('// 4. DASHBOARD SCREEN')

    if start_idx != -1 and end_idx != -1:
        content = content[:start_idx] + content[end_idx:]

    with open('econosense_app/lib/main.dart', 'w', encoding='utf-8') as f:
        f.write(content)

    print('Refactor successful')

if __name__ == '__main__':
    refactor()
