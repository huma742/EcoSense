import re

def fix():
    with open('econosense_app/lib/main.dart', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update ProfileScreen constructor
    profile_target = """class ProfileScreen extends StatefulWidget {
  final String userName;
  final String userEmail;
  final VoidCallback onLogout;

  const ProfileScreen({super.key, required this.userName, required this.userEmail, required this.onLogout});"""
    profile_replace = """class ProfileScreen extends StatefulWidget {
  final String userName;
  final String userEmail;
  final VoidCallback onLogout;
  final List<Map<String, dynamic>> recentActions;

  const ProfileScreen({super.key, required this.userName, required this.userEmail, required this.onLogout, this.recentActions = const []});"""
    content = content.replace(profile_target, profile_replace)

    # 2. Update DashboardScreen to pass recentActions to ProfileScreen
    ds_target = """      ProfileScreen(userName: _userName, userEmail: _userEmail, onLogout: _logout),"""
    ds_replace = """      ProfileScreen(userName: _userName, userEmail: _userEmail, onLogout: _logout, recentActions: _recentActions),"""
    content = content.replace(ds_target, ds_replace)

    # 3. Update ProfileScreen build method stats
    ps_stats_target = """            Transform.translate(
              offset: const Offset(0, -20),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
                child: Row(
                  children: [
                    Expanded(child: _buildStatCard('Analyses', '12', Icons.insert_chart, const Color(0xFF2E7D32))),
                    const SizedBox(width: 12),
                    Expanded(child: _buildStatCard('Avg Risk', '6.5', Icons.warning, const Color(0xFFF57C00))),
                    const SizedBox(width: 12),
                    Expanded(child: _buildStatCard('Active', '3d', Icons.calendar_today, const Color(0xFF1565C0))),
                  ],
                ),
              ),
            ),"""
    ps_stats_replace = """            Transform.translate(
              offset: const Offset(0, -20),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
                child: Row(
                  children: [
                    Expanded(child: _buildStatCard('Analyses', '${widget.recentActions.length}', Icons.insert_chart, const Color(0xFF2E7D32))),
                    const SizedBox(width: 12),
                    Expanded(child: _buildStatCard('Avg Risk', (widget.recentActions.isEmpty ? 0.0 : widget.recentActions.fold(0.0, (sum, a) => sum + (a['risk_score'] as double? ?? 0.0)) / widget.recentActions.length).toStringAsFixed(1), Icons.warning, const Color(0xFFF57C00))),
                    const SizedBox(width: 12),
                    Expanded(child: _buildStatCard('Active Days', '3d', Icons.calendar_today, const Color(0xFF1565C0))),
                  ],
                ),
              ),
            ),"""
    content = content.replace(ps_stats_target, ps_stats_replace)

    # 4. Update DashboardHome stats
    dh_stats_target = """            Row(
              children: [
                Expanded(child: _buildStatCard('Actions Executed', '${recentActions.length}', Icons.insert_chart, Colors.blue)),
              ],
            ),"""
    dh_stats_replace = """            Row(
              children: [
                Expanded(child: _buildStatCard('Actions Executed', '${recentActions.length}', Icons.insert_chart, Colors.blue)),
                const SizedBox(width: 16),
                Expanded(child: _buildStatCard('Avg Risk', (recentActions.isEmpty ? 0.0 : recentActions.fold(0.0, (sum, a) => sum + (a['risk_score'] as double? ?? 0.0)) / recentActions.length).toStringAsFixed(1), Icons.warning, Colors.orange)),
              ],
            ),"""
    content = content.replace(dh_stats_target, dh_stats_replace)

    # 5. Update _executeAction to save riskScore
    exec_target = """  Future<void> _executeAction(BuildContext context, Map<String, dynamic> topAction, String eventTitle) async {"""
    exec_replace = """  Future<void> _executeAction(BuildContext context, Map<String, dynamic> topAction, String eventTitle, int riskScore) async {"""
    content = content.replace(exec_target, exec_replace)
    
    exec_call_target = """onPressed: () => _executeAction(context, actions[0], insights['event'] ?? 'Analysis'),"""
    exec_call_replace = """onPressed: () => _executeAction(context, actions[0], insights['event'] ?? 'Analysis', riskScore),"""
    content = content.replace(exec_call_target, exec_call_replace)

    new_exec_target = """    final newExecution = {
      'title': eventTitle,
      'subtitle': topAction['description'] ?? 'Action executed successfully.',
      'time': '${DateTime.now().hour}:${DateTime.now().minute.toString().padLeft(2, '0')}',
      'priority': topAction['priority'] ?? 'LOW',
    };"""
    new_exec_replace = """    final newExecution = {
      'title': eventTitle,
      'subtitle': topAction['description'] ?? 'Action executed successfully.',
      'time': '${DateTime.now().hour}:${DateTime.now().minute.toString().padLeft(2, '0')}',
      'priority': topAction['priority'] ?? 'LOW',
      'risk_score': riskScore.toDouble(),
    };"""
    content = content.replace(new_exec_target, new_exec_replace)
    
    load_user_list_target = """  List<Map<String, String>> _recentActions = [];"""
    load_user_list_replace = """  List<Map<String, dynamic>> _recentActions = [];"""
    content = content.replace(load_user_list_target, load_user_list_replace)
    
    load_user_parsed_target = """    List<Map<String, String>> parsedActions = [];"""
    load_user_parsed_replace = """    List<Map<String, dynamic>> parsedActions = [];"""
    content = content.replace(load_user_parsed_target, load_user_parsed_replace)
    
    dh_list_target = """  final List<Map<String, String>> recentActions;

  const DashboardHome({super.key, required this.userName, required this.onLogout, this.recentActions = const []});"""
    dh_list_replace = """  final List<Map<String, dynamic>> recentActions;

  const DashboardHome({super.key, required this.userName, required this.onLogout, this.recentActions = const []});"""
    content = content.replace(dh_list_target, dh_list_replace)

    # 6. Re-add LoginScreen & SignupScreen
    login_signup_code = """
// -----------------------------------------------------------------------------
// LOGIN & SIGNUP SCREENS
// -----------------------------------------------------------------------------
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  Future<void> _login() async {
    final prefs = await SharedPreferences.getInstance();
    // Use previously saved name/email if exists, otherwise fallback
    final existingName = prefs.getString('name') ?? 'Analyst';
    final existingEmail = prefs.getString('email') ?? _emailController.text.trim();
    await prefs.setString('name', existingName);
    await prefs.setString('email', existingEmail);
    await prefs.setBool('isLoggedIn', true);
    if (mounted) {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const DashboardScreen()));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.analytics, size: 80, color: Color(0xFF2E7D32)),
              const SizedBox(height: 24),
              const Text('Welcome Back', textAlign: TextAlign.center, style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
              const SizedBox(height: 32),
              TextField(controller: _emailController, decoration: const InputDecoration(labelText: 'Email', prefixIcon: Icon(Icons.email))),
              const SizedBox(height: 16),
              TextField(controller: _passwordController, obscureText: true, decoration: const InputDecoration(labelText: 'Password', prefixIcon: Icon(Icons.lock))),
              const SizedBox(height: 32),
              ElevatedButton(onPressed: _login, child: const Text('Login', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold))),
              TextButton(
                onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SignupScreen())),
                child: const Text('Don\\'t have an account? Sign Up', style: TextStyle(color: Color(0xFF2E7D32))),
              )
            ],
          ),
        ),
      ),
    );
  }
}

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});
  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  Future<void> _signup() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('name', _nameController.text.trim());
    await prefs.setString('email', _emailController.text.trim());
    await prefs.setBool('isLoggedIn', true);
    if (mounted) {
      Navigator.pushAndRemoveUntil(context, MaterialPageRoute(builder: (_) => const DashboardScreen()), (route) => false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(backgroundColor: Colors.white, elevation: 0, leading: const BackButton(color: Color(0xFF2E7D32))),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text('Create Account', textAlign: TextAlign.center, style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
              const SizedBox(height: 32),
              TextField(controller: _nameController, decoration: const InputDecoration(labelText: 'Full Name', prefixIcon: Icon(Icons.person))),
              const SizedBox(height: 16),
              TextField(controller: _emailController, decoration: const InputDecoration(labelText: 'Email', prefixIcon: Icon(Icons.email))),
              const SizedBox(height: 16),
              TextField(controller: _passwordController, obscureText: true, decoration: const InputDecoration(labelText: 'Password', prefixIcon: Icon(Icons.lock))),
              const SizedBox(height: 32),
              ElevatedButton(onPressed: _signup, child: const Text('Sign Up', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold))),
            ],
          ),
        ),
      ),
    );
  }
}
"""
    content = content.replace("class DashboardScreen extends StatefulWidget {", login_signup_code + "\nclass DashboardScreen extends StatefulWidget {")

    # 7. Update SplashScreen & Logout logic
    splash_target = """    if (mounted) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const DashboardScreen()),
      );
    }"""
    splash_replace = """    if (mounted) {
      final prefs = await SharedPreferences.getInstance();
      final bool isLoggedIn = prefs.getBool('isLoggedIn') ?? false;
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => isLoggedIn ? const DashboardScreen() : const LoginScreen()),
      );
    }"""
    content = content.replace(splash_target, splash_replace)

    logout_target = """  Future<void> _logout() async {
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Logout disabled in this version')));
  }"""
    logout_replace = """  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    if (mounted) {
      Navigator.pushAndRemoveUntil(context, MaterialPageRoute(builder: (_) => const LoginScreen()), (route) => false);
    }
  }"""
    content = content.replace(logout_target, logout_replace)
    
    # 8. Extract risk_score in _loadUser
    load_user_parsing_target = """        parsedActions.add({
          'title': (decoded['event'] ?? decoded['title']).toString(),
          'subtitle': decoded['subtitle'].toString(),
          'time': decoded['time'].toString(),
          'priority': decoded['priority']?.toString() ?? 'LOW',
        });"""
    load_user_parsing_replace = """        parsedActions.add({
          'title': (decoded['event'] ?? decoded['title']).toString(),
          'subtitle': decoded['subtitle'].toString(),
          'time': decoded['time'].toString(),
          'priority': decoded['priority']?.toString() ?? 'LOW',
          'risk_score': double.tryParse(decoded['risk_score']?.toString() ?? '0.0') ?? 0.0,
        });"""
    content = content.replace(load_user_parsing_target, load_user_parsing_replace)

    with open('econosense_app/lib/main.dart', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix()
