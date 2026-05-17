import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:file_picker/file_picker.dart';
import 'package:syncfusion_flutter_pdf/pdf.dart';
import 'dart:convert';
import 'dart:async';
import 'dart:io';

void main() {
  runApp(const EconoSenseApp());
}

class EconoSenseApp extends StatelessWidget {
  const EconoSenseApp({super.key});


  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EconoSense PK',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2E7D32),
          primary: const Color(0xFF2E7D32),
          secondary: const Color(0xFF81C784),
        ),
        useMaterial3: true,
        scaffoldBackgroundColor: Colors.grey[50],
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF2E7D32),
          foregroundColor: Colors.white,
          elevation: 0,
          centerTitle: true,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFF2E7D32),
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            padding: const EdgeInsets.symmetric(vertical: 16),
            elevation: 2,
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: Colors.grey.shade300),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: Colors.grey.shade300),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Color(0xFF2E7D32), width: 2),
          ),
        ),
      ),
      home: const SplashScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

// -----------------------------------------------------------------------------
// 1. SPLASH SCREEN
// -----------------------------------------------------------------------------
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..forward();
    _animation = CurvedAnimation(parent: _controller, curve: Curves.easeInOut);

    _startTimer();
  }

  Future<void> _startTimer() async {
    // Show splash screen for exactly 3 seconds
    await Future.delayed(const Duration(seconds: 3));
    
    final prefs = await SharedPreferences.getInstance();
    final bool isLoggedIn = prefs.getBool('isLoggedIn') ?? false;
    if (mounted) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => isLoggedIn ? const DashboardScreen() : const LoginScreen()),
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF2E7D32),
      body: Center(
        child: FadeTransition(
          opacity: _animation,
          child: ScaleTransition(
            scale: _animation,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.trending_up, size: 80, color: Color(0xFF2E7D32)),
                ),
                const SizedBox(height: 24),
                const Text(
                  'EconoSense PK',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.2,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'Agentic AI System',
                  style: TextStyle(
                    color: Colors.green[100],
                    fontSize: 18,
                    letterSpacing: 2,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// -----------------------------------------------------------------------------
// 4. DASHBOARD SCREEN
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
// LOGIN & SIGNUP SCREENS
// -----------------------------------------------------------------------------
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> with SingleTickerProviderStateMixin {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscureText = true;
  
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(duration: const Duration(milliseconds: 800), vsync: this);
    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(_animationController);
    _slideAnimation = Tween<Offset>(begin: const Offset(0.0, 0.2), end: Offset.zero).animate(CurvedAnimation(parent: _animationController, curve: Curves.easeOutQuart));
    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

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

  Widget _buildBackground() {
    return Stack(
      children: [
        Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF1B5E20), Color(0xFF00695C), Color(0xFF1A237E)],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
            ),
          ),
        ),
        Positioned(
          top: -50,
          left: -50,
          child: Container(
            width: 200, height: 200,
            decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withOpacity(0.1)),
          )
        ),
        Positioned(
          top: 200,
          right: -80,
          child: Container(
            width: 300, height: 300,
            decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withOpacity(0.1)),
          )
        ),
        Positioned(
          bottom: -100,
          left: 50,
          child: Container(
            width: 250, height: 250,
            decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withOpacity(0.1)),
          )
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          _buildBackground(),
          SafeArea(
            child: Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 24.0),
                child: FadeTransition(
                  opacity: _fadeAnimation,
                  child: SlideTransition(
                    position: _slideAnimation,
                    child: Container(
                      padding: const EdgeInsets.all(28.0),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(24.0),
                        boxShadow: const [
                          BoxShadow(color: Colors.black38, blurRadius: 15, offset: Offset(0, 8)),
                        ],
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: const [
                              Icon(Icons.insert_chart_outlined, color: Color(0xFF1B5E20), size: 32),
                              SizedBox(width: 8),
                              Text('EconoSense PK', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF1B5E20))),
                            ],
                          ),
                          const SizedBox(height: 32),
                          const Text('Login', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.black)),
                          const SizedBox(height: 8),
                          const Text('Sign in to continue', style: TextStyle(fontSize: 16, color: Colors.grey)),
                          const SizedBox(height: 32),
                          
                          TextField(
                            controller: _emailController, 
                            decoration: InputDecoration(
                              hintText: 'Username',
                              hintStyle: const TextStyle(color: Colors.grey),
                              prefixIcon: const Icon(Icons.person, color: Colors.grey),
                              filled: true,
                              fillColor: Colors.grey[200],
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
                            )
                          ),
                          const SizedBox(height: 16),
                          
                          TextField(
                            controller: _passwordController, 
                            obscureText: _obscureText, 
                            decoration: InputDecoration(
                              hintText: 'Password',
                              hintStyle: const TextStyle(color: Colors.grey),
                              prefixIcon: const Icon(Icons.lock, color: Colors.grey),
                              filled: true,
                              fillColor: Colors.grey[200],
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
                              suffixIcon: IconButton(
                                icon: Icon(_obscureText ? Icons.visibility_off : Icons.visibility, color: Colors.grey),
                                onPressed: () {
                                  setState(() {
                                    _obscureText = !_obscureText;
                                  });
                                },
                              ),
                            )
                          ),
                          const SizedBox(height: 32),
                          
                          Container(
                            decoration: BoxDecoration(
                              gradient: const LinearGradient(colors: [Color(0xFF1B5E20), Color(0xFF00695C)]),
                              borderRadius: BorderRadius.circular(16),
                              boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 6, offset: Offset(0, 3))],
                            ),
                            child: ElevatedButton(
                              onPressed: _login, 
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.transparent,
                                shadowColor: Colors.transparent,
                                padding: const EdgeInsets.symmetric(vertical: 18),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                              ),
                              child: const Text('LOGIN', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                            ),
                          ),
                          const SizedBox(height: 24),
                          Center(
                            child: GestureDetector(
                              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SignupScreen())),
                              child: const Text("Don't have an account? Sign up", style: TextStyle(color: Color(0xFF1B5E20), fontSize: 14, fontWeight: FontWeight.bold)),
                            ),
                          )
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});
  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> with SingleTickerProviderStateMixin {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscureText = true;
  
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(duration: const Duration(milliseconds: 800), vsync: this);
    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(_animationController);
    // slide from right
    _slideAnimation = Tween<Offset>(begin: const Offset(0.2, 0.0), end: Offset.zero).animate(CurvedAnimation(parent: _animationController, curve: Curves.easeOutQuart));
    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _signup() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('name', _nameController.text.trim());
    await prefs.setString('email', _emailController.text.trim());
    await prefs.setBool('isLoggedIn', true);
    if (mounted) {
      Navigator.pushAndRemoveUntil(context, MaterialPageRoute(builder: (_) => const DashboardScreen()), (route) => false);
    }
  }

  Widget _buildBackground() {
    return Stack(
      children: [
        Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF1B5E20), Color(0xFF00695C), Color(0xFF1A237E)],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
            ),
          ),
        ),
        Positioned(
          top: -50,
          left: -50,
          child: Container(
            width: 200, height: 200,
            decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withOpacity(0.1)),
          )
        ),
        Positioned(
          top: 200,
          right: -80,
          child: Container(
            width: 300, height: 300,
            decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withOpacity(0.1)),
          )
        ),
        Positioned(
          bottom: -100,
          left: 50,
          child: Container(
            width: 250, height: 250,
            decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withOpacity(0.1)),
          )
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          _buildBackground(),
          SafeArea(
            child: Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 24.0),
                child: FadeTransition(
                  opacity: _fadeAnimation,
                  child: SlideTransition(
                    position: _slideAnimation,
                    child: Container(
                      padding: const EdgeInsets.all(28.0),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(24.0),
                        boxShadow: const [
                          BoxShadow(color: Colors.black38, blurRadius: 15, offset: Offset(0, 8)),
                        ],
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: const [
                              Icon(Icons.insert_chart_outlined, color: Color(0xFF1B5E20), size: 32),
                              SizedBox(width: 8),
                              Text('EconoSense PK', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF1B5E20))),
                            ],
                          ),
                          const SizedBox(height: 32),
                          const Text('Create Account', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.black)),
                          const SizedBox(height: 8),
                          GestureDetector(
                            onTap: () => Navigator.pop(context),
                            child: const Text('Already registered? Log in here', style: TextStyle(fontSize: 14, color: Color(0xFF1B5E20), fontWeight: FontWeight.bold)),
                          ),
                          const SizedBox(height: 32),
                          
                          TextField(
                            controller: _nameController, 
                            decoration: InputDecoration(
                              hintText: 'Name',
                              hintStyle: const TextStyle(color: Colors.grey),
                              prefixIcon: const Icon(Icons.person, color: Colors.grey),
                              filled: true,
                              fillColor: Colors.grey[200],
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
                            )
                          ),
                          const SizedBox(height: 16),

                          TextField(
                            controller: _emailController, 
                            decoration: InputDecoration(
                              hintText: 'Email',
                              hintStyle: const TextStyle(color: Colors.grey),
                              prefixIcon: const Icon(Icons.email, color: Colors.grey),
                              filled: true,
                              fillColor: Colors.grey[200],
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
                            )
                          ),
                          const SizedBox(height: 16),
                          
                          TextField(
                            controller: _passwordController, 
                            obscureText: _obscureText, 
                            decoration: InputDecoration(
                              hintText: 'Password',
                              hintStyle: const TextStyle(color: Colors.grey),
                              prefixIcon: const Icon(Icons.lock, color: Colors.grey),
                              filled: true,
                              fillColor: Colors.grey[200],
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
                              suffixIcon: IconButton(
                                icon: Icon(_obscureText ? Icons.visibility_off : Icons.visibility, color: Colors.grey),
                                onPressed: () {
                                  setState(() {
                                    _obscureText = !_obscureText;
                                  });
                                },
                              ),
                            )
                          ),
                          const SizedBox(height: 32),
                          
                          Container(
                            decoration: BoxDecoration(
                              gradient: const LinearGradient(colors: [Color(0xFF1B5E20), Color(0xFF00695C)]),
                              borderRadius: BorderRadius.circular(16),
                              boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 6, offset: Offset(0, 3))],
                            ),
                            child: ElevatedButton(
                              onPressed: _signup, 
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.transparent,
                                shadowColor: Colors.transparent,
                                padding: const EdgeInsets.symmetric(vertical: 18),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                              ),
                              child: const Text('REGISTER', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _currentIndex = 0;
  String _userName = 'Analyst';
  String _userEmail = 'analyst@econosense.pk';
  List<Map<String, dynamic>> _recentActions = [];

  @override
  void initState() {
    super.initState();
    _loadUser();
  }

  Future<void> _loadUser() async {
    final prefs = await SharedPreferences.getInstance();
    final savedActions = prefs.getStringList('executed_actions') ?? [];
    
    List<Map<String, dynamic>> parsedActions = [];
    for (var actionStr in savedActions) {
      try {
        final Map<String, dynamic> decoded = jsonDecode(actionStr);
        parsedActions.add({
          'title': (decoded['event'] ?? decoded['title']).toString(),
          'subtitle': decoded['subtitle'].toString(),
          'time': decoded['time'].toString(),
          'priority': decoded['priority']?.toString() ?? 'LOW',
          'risk_score': double.tryParse(decoded['risk_score']?.toString() ?? '0.0') ?? 0.0,
        });
      } catch(e) {}
    }
    
    setState(() {
      _userName = prefs.getString('name') ?? 'Analyst';
      _userEmail = prefs.getString('email') ?? 'analyst@econosense.pk';
      _recentActions = parsedActions.reversed.toList(); // Newest first
    });
  }

  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isLoggedIn', false);
    if (mounted) {
      Navigator.pushAndRemoveUntil(context, MaterialPageRoute(builder: (_) => const LoginScreen()), (route) => false);
    }
  }



  @override
  Widget build(BuildContext context) {
    final List<Widget> screens = [
      DashboardHome(userName: _userName, onLogout: _logout, recentActions: _recentActions),
      const AnalyzeScreen(),
      ProfileScreen(userName: _userName, userEmail: _userEmail, onLogout: _logout, recentActions: _recentActions),
    ];

    return Scaffold(
      body: screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() => _currentIndex = index);
          if (index == 0) _loadUser();
        },
        selectedItemColor: const Color(0xFF1B5E20),
        unselectedItemColor: Colors.grey,
        backgroundColor: Colors.white,
        elevation: 10,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.dashboard), label: 'Dashboard'),
          BottomNavigationBarItem(icon: Icon(Icons.analytics), label: 'Analyze'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}

class DashboardHome extends StatelessWidget {
  final String userName;
  final VoidCallback onLogout;
  final List<Map<String, dynamic>> recentActions;

  const DashboardHome({super.key, required this.userName, required this.onLogout, this.recentActions = const []});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      body: Column(
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.only(top: 60, left: 24, right: 24, bottom: 32),
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF1B5E20), Color(0xFF00695C)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.only(
                bottomLeft: Radius.circular(30),
                bottomRight: Radius.circular(30),
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('Dashboard', style: TextStyle(color: Colors.white70, fontSize: 16)),
                    IconButton(icon: const Icon(Icons.logout, color: Colors.white), onPressed: onLogout),
                  ],
                ),
                const SizedBox(height: 8),
                Text('Welcome back, $userName!', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white)),
              ],
            ),
          ),
          
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(child: _buildStatCard('Actions Executed', '${recentActions.length}', Icons.insert_chart, const [Color(0xFF43A047), Color(0xFF1B5E20)])),
                      const SizedBox(width: 16),
                      Expanded(child: _buildStatCard('Avg Risk', (recentActions.isEmpty ? 0.0 : recentActions.fold(0.0, (sum, a) => sum + (a['risk_score'] as double? ?? 0.0)) / recentActions.length).toStringAsFixed(1), Icons.warning, const [Color(0xFFFFB74D), Color(0xFFF57C00)])),
                    ],
                  ),
                  const SizedBox(height: 32),
                  const Text('Recent Executed Actions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black87)),
                  const SizedBox(height: 16),
                  if (recentActions.isEmpty)
                    _buildRecentCard('No actions executed yet', 'Run analysis and execute an action', 'Now')
                  else
                    ...recentActions.map((action) => _buildRecentCard(action['title'] ?? '', action['subtitle'] ?? '', action['time'] ?? '', action['priority'] ?? 'LOW')).toList(),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, List<Color> gradientColors) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: gradientColors, begin: Alignment.topLeft, end: Alignment.bottomRight),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: gradientColors.last.withOpacity(0.4), blurRadius: 10, offset: const Offset(0, 4))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: Colors.white, size: 32),
          const SizedBox(height: 16),
          Text(value, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white)),
          const SizedBox(height: 4),
          Text(title, style: const TextStyle(color: Colors.white70, fontSize: 14)),
        ],
      ),
    );
  }

  Widget _buildRecentCard(String title, String subtitle, String time, [String priority = 'LOW']) {
    Color priorityColor;
    switch (priority.toUpperCase()) {
      case 'HIGH': priorityColor = Colors.red; break;
      case 'MED': priorityColor = Colors.orange; break;
      case 'LOW': priorityColor = Colors.blue; break;
      default: priorityColor = Colors.grey;
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4))],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: Container(
          decoration: const BoxDecoration(
            border: Border(left: BorderSide(color: Color(0xFF1B5E20), width: 6)),
          ),
          child: ListTile(
            contentPadding: const EdgeInsets.all(16),
            leading: Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(color: Colors.green.shade50, shape: BoxShape.circle),
              child: const Icon(Icons.check_circle, color: Color(0xFF1B5E20)),
            ),
            title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16), maxLines: 2, overflow: TextOverflow.ellipsis),
            subtitle: Padding(
              padding: const EdgeInsets.only(top: 8.0),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Text(subtitle, maxLines: 2, overflow: TextOverflow.ellipsis, style: TextStyle(color: Colors.grey[600])),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: priorityColor.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      priority,
                      style: TextStyle(color: priorityColor, fontWeight: FontWeight.bold, fontSize: 10),
                    ),
                  ),
                ],
              ),
            ),
            trailing: Text(time, style: const TextStyle(fontSize: 12, color: Colors.grey, fontWeight: FontWeight.bold)),
          ),
        ),
      ),
    );
  }
}

class ProfileScreen extends StatefulWidget {
  final String userName;
  final String userEmail;
  final VoidCallback onLogout;
  final List<Map<String, dynamic>> recentActions;

  const ProfileScreen({super.key, required this.userName, required this.userEmail, required this.onLogout, this.recentActions = const []});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  bool _notificationsEnabled = true;
  bool _darkModeEnabled = false;

  String _getInitials(String name) {
    if (name.isEmpty) return "A";
    List<String> parts = name.split(" ");
    if (parts.length > 1) {
      return "${parts[0][0]}${parts[1][0]}".toUpperCase();
    }
    return name[0].toUpperCase();
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.only(top: 60, bottom: 40),
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  colors: [Color(0xFF1B5E20), Color(0xFF00695C)],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                ),
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(40),
                  bottomRight: Radius.circular(40),
                ),
              ),
              child: Column(
                children: [
                  CircleAvatar(
                    radius: 50,
                    backgroundColor: Colors.white,
                    child: Text(
                      _getInitials(widget.userName),
                      style: const TextStyle(fontSize: 36, fontWeight: FontWeight.bold, color: Color(0xFF1B5E20)),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    widget.userName,
                    style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    widget.userEmail,
                    style: TextStyle(fontSize: 16, color: Colors.green[100]),
                  ),
                ],
              ),
            ),
            
            Transform.translate(
              offset: const Offset(0, -20),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20.0),
                child: Row(
                  children: [
                    Expanded(child: _buildStatCard('Analyses', '${widget.recentActions.length}', Icons.insert_chart, const Color(0xFF2E7D32))),
                    const SizedBox(width: 12),
                    Expanded(child: _buildStatCard('Avg Risk', (widget.recentActions.isEmpty ? 0.0 : widget.recentActions.fold(0.0, (sum, a) => sum + (a['risk_score'] as double? ?? 0.0)) / widget.recentActions.length).toStringAsFixed(1), Icons.warning, const Color(0xFFF57C00))),
                    const SizedBox(width: 12),
                    Expanded(child: _buildStatCard('Active', '3d', Icons.calendar_today, const Color(0xFF1565C0))),
                  ],
                ),
              ),
            ),

            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Settings', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black87)),
                  const SizedBox(height: 16),
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4))],
                    ),
                    child: Column(
                      children: [
                        ListTile(
                          leading: Container(padding: const EdgeInsets.all(8), decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(10)), child: const Icon(Icons.person_outline, color: Color(0xFF1B5E20))),
                          title: const Text('Account Settings', style: TextStyle(fontWeight: FontWeight.w600)),
                          trailing: const Icon(Icons.chevron_right, color: Colors.grey),
                          onTap: () {},
                        ),
                        Divider(height: 1, color: Colors.grey[200]),
                        SwitchListTile(
                          secondary: Container(padding: const EdgeInsets.all(8), decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(10)), child: const Icon(Icons.notifications_outlined, color: Color(0xFF1B5E20))),
                          title: const Text('Notifications', style: TextStyle(fontWeight: FontWeight.w600)),
                          value: _notificationsEnabled,
                          activeColor: const Color(0xFF1B5E20),
                          onChanged: (val) => setState(() => _notificationsEnabled = val),
                        ),
                        Divider(height: 1, color: Colors.grey[200]),
                        SwitchListTile(
                          secondary: Container(padding: const EdgeInsets.all(8), decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(10)), child: const Icon(Icons.dark_mode_outlined, color: Color(0xFF1B5E20))),
                          title: const Text('Dark Mode', style: TextStyle(fontWeight: FontWeight.w600)),
                          value: _darkModeEnabled,
                          activeColor: const Color(0xFF1B5E20),
                          onChanged: (val) => setState(() => _darkModeEnabled = val),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 32),
                  const Text('More', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black87)),
                  const SizedBox(height: 16),
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4))],
                    ),
                    child: Column(
                      children: [
                        ListTile(
                          leading: Container(padding: const EdgeInsets.all(8), decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(10)), child: const Icon(Icons.info_outline, color: Color(0xFF1B5E20))),
                          title: const Text('About App', style: TextStyle(fontWeight: FontWeight.w600)),
                          trailing: const Text('v1.0.0', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
                          onTap: () {},
                        ),
                        Divider(height: 1, color: Colors.grey[200]),
                        ListTile(
                          leading: Container(padding: const EdgeInsets.all(8), decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(10)), child: const Icon(Icons.privacy_tip_outlined, color: Color(0xFF1B5E20))),
                          title: const Text('Privacy Policy', style: TextStyle(fontWeight: FontWeight.w600)),
                          trailing: const Icon(Icons.chevron_right, color: Colors.grey),
                          onTap: () {},
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 32),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red[50],
                        foregroundColor: Colors.red,
                        elevation: 0,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                      icon: const Icon(Icons.logout),
                      label: const Text('Log Out', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      onPressed: widget.onLogout,
                    ),
                  ),
                  const SizedBox(height: 40),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 8),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: color.withOpacity(0.4),
            blurRadius: 15,
            offset: const Offset(0, 6),
          )
        ],
      ),
      child: Column(
        children: [
          Icon(icon, color: Colors.white, size: 36),
          const SizedBox(height: 12),
          Text(value, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold, color: Colors.white)),
          const SizedBox(height: 4),
          Text(title, textAlign: TextAlign.center, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}

// -----------------------------------------------------------------------------
// 5. ANALYZE SCREEN (TEXT, URL, PDF)
// -----------------------------------------------------------------------------
class AnalyzeScreen extends StatefulWidget {
  const AnalyzeScreen({super.key});

  @override
  State<AnalyzeScreen> createState() => _AnalyzeScreenState();
}

class _AnalyzeScreenState extends State<AnalyzeScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final TextEditingController _textController = TextEditingController();
  final TextEditingController _urlController = TextEditingController();
  final TextEditingController _source1Controller = TextEditingController();
  final TextEditingController _source2Controller = TextEditingController();
  final TextEditingController _source3Controller = TextEditingController();
  final TextEditingController _csvController = TextEditingController();
  Timer? _feedTimer;
  int _feedIndex = 1;
  final List<String> _possibleHeadlines = [
    "State Bank of Pakistan raises interest rates by 100bps to curb inflation",
    "Pakistan's trade deficit narrows by 12% in Q1 2026 amid export growth",
    "IMF approves \$1.2 billion tranche for Pakistan under bailout program",
    "FBR reports 15% increase in tax revenue collection this fiscal quarter",
    "Pakistan Stock Exchange gains 800 points as foreign investment rises"
  ];
  List<String> _liveFeedItems = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _liveFeedItems = [_possibleHeadlines[0]];
    _tabController = TabController(length: 6, vsync: this);
    _feedTimer = Timer.periodic(const Duration(seconds: 30), (timer) {
      if (mounted) {
        setState(() {
          if (!_liveFeedItems.contains(_possibleHeadlines[_feedIndex])) {
            _liveFeedItems.insert(0, _possibleHeadlines[_feedIndex]);
          }
          _feedIndex = (_feedIndex + 1) % _possibleHeadlines.length;
          if (_liveFeedItems.length > 5) {
            _liveFeedItems.removeLast();
          }
        });
      }
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    _textController.dispose();
    _urlController.dispose();
    _source1Controller.dispose();
    _source2Controller.dispose();
    _source3Controller.dispose();
    _csvController.dispose();
    _feedTimer?.cancel();
    super.dispose();
  }

  // --- 1. Base API Call ---
  Future<void> _sendToBackend(String text) async {
    if (text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('No text to analyze')));
      return;
    }

    try {
      final uri = Uri.parse('http://192.168.100.20:8000/analyze'); // or 10.0.2.2 for Android emulator
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'news_text': text}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (!mounted) return;
        Navigator.push(context, MaterialPageRoute(builder: (_) => ResultsScreen(data: data)));
      } else {
        throw Exception('Server Error: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Analysis failed: $e'), backgroundColor: Colors.red),
      );
    }
  }

  // --- 2. Text Input ---
  Future<void> _analyzeText() async {
    final text = _textController.text.trim();
    if (text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Please enter some text')));
      return;
    }
    setState(() => _isLoading = true);
    await _sendToBackend(text);
    if (mounted) setState(() => _isLoading = false);
  }

  // --- 3. URL Fetch ---
  Future<void> _analyzeUrl() async {
    final urlStr = _urlController.text.trim();
    if (urlStr.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Please enter a URL')));
      return;
    }

    setState(() => _isLoading = true);
    try {
      final uri = Uri.parse('http://192.168.100.20:8000/analyze-url'); // or 10.0.2.2 for Android emulator
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'url': urlStr}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (!mounted) return;
        Navigator.push(context, MaterialPageRoute(builder: (_) => ResultsScreen(data: data)));
      } else {
        throw Exception('Server Error: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('URL Error: $e'), backgroundColor: Colors.red));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  // --- 4. PDF Upload ---
  Future<void> _pickAndAnalyzePdf() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf'],
        withData: true,
      );

      if (result != null && result.files.single.path != null) {
        setState(() => _isLoading = true);
        
        List<int> bytes;
        if (result.files.single.bytes != null) {
          bytes = result.files.single.bytes!;
        } else {
          bytes = File(result.files.single.path!).readAsBytesSync();
        }

        // Extract text
        final PdfDocument document = PdfDocument(inputBytes: bytes);
        final PdfTextExtractor extractor = PdfTextExtractor(document);
        final String text = extractor.extractText();
        document.dispose();

        if (text.trim().isEmpty) {
          throw Exception("Could not extract any text from the PDF. It might be scanned/images.");
        }

        await _sendToBackend(text.substring(0, text.length > 5000 ? 5000 : text.length)); // Limit text size

      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('PDF Error: $e'), backgroundColor: Colors.red));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.only(top: 50),
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF1B5E20), Color(0xFF00695C)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Column(
              children: [
                const Padding(
                  padding: EdgeInsets.symmetric(vertical: 16.0),
                  child: Text('Analyze', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
                ),
                Container(
                  color: Colors.white,
                  child: TabBar(
                    controller: _tabController,
                    indicatorColor: const Color(0xFF1B5E20),
                    indicatorWeight: 4,
                    labelColor: const Color(0xFF1B5E20),
                    unselectedLabelColor: Colors.grey,
                    isScrollable: true,
                    tabs: const [
                      Tab(text: 'Text'),
                      Tab(text: 'URL'),
                      Tab(text: 'PDF'),
                      Tab(text: 'Multi'),
                      Tab(text: 'CSV'),
                      Tab(text: 'Feed'),
                    ],
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: [
                _buildTextTab(),
                _buildUrlTab(),
                _buildPdfTab(),
                _buildMultiSourceTab(),
                _buildCsvTab(),
                _buildFeedTab(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  InputDecoration _getInputDecoration(String hint, {IconData? prefixIcon}) {
    return InputDecoration(
      hintText: hint,
      hintStyle: const TextStyle(color: Colors.grey),
      prefixIcon: prefixIcon != null ? Icon(prefixIcon, color: Colors.grey) : null,
      filled: true,
      fillColor: Colors.grey[200],
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
      enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
      focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
      contentPadding: const EdgeInsets.all(20),
    );
  }

  Widget _buildTextTab() {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            child: TextField(
              controller: _textController,
              maxLines: null,
              expands: true,
              textAlignVertical: TextAlignVertical.top,
              decoration: _getInputDecoration('Paste economic news text here...'),
            ),
          ),
          const SizedBox(height: 24),
          _buildAnalyzeButton('Analyze Text', _analyzeText),
        ],
      ),
    );
  }

  Widget _buildUrlTab() {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const SizedBox(height: 24),
          const Text('Extract news from a URL', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black87)),
          const SizedBox(height: 16),
          TextField(
            controller: _urlController,
            decoration: _getInputDecoration('https://example.com/news-article', prefixIcon: Icons.link),
          ),
          const Spacer(),
          _buildAnalyzeButton('Fetch & Analyze URL', _analyzeUrl),
        ],
      ),
    );
  }

  Widget _buildPdfTab() {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Spacer(),
          Container(
            padding: const EdgeInsets.all(40),
            decoration: BoxDecoration(color: Colors.green.shade50, shape: BoxShape.circle),
            child: const Icon(Icons.picture_as_pdf, size: 80, color: Color(0xFF1B5E20)),
          ),
          const SizedBox(height: 32),
          const Text(
            'Upload a PDF report for analysis',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black87),
          ),
          const SizedBox(height: 16),
          const Text(
            'We will extract the text and analyze economic indicators.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey),
          ),
          const Spacer(),
          _buildAnalyzeButton('Select PDF & Analyze', _pickAndAnalyzePdf),
        ],
      ),
    );
  }


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
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text('Analyze multiple sources for contradictions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black87)),
                  const SizedBox(height: 24),
                  TextField(controller: _source1Controller, maxLines: 4, decoration: _getInputDecoration('Source 1 text...')),
                  const SizedBox(height: 16),
                  TextField(controller: _source2Controller, maxLines: 4, decoration: _getInputDecoration('Source 2 text...')),
                  const SizedBox(height: 16),
                  TextField(controller: _source3Controller, maxLines: 4, decoration: _getInputDecoration('Source 3 text (optional)...')),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          _buildAnalyzeButton('Analyze Multiple Sources', _analyzeMulti),
        ],
      ),
    );
  }


  // --- 6. CSV/JSON ---
  Future<void> _analyzeCsv() async {
    final text = _csvController.text.trim();
    if (text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Please enter CSV or JSON data')));
      return;
    }
    setState(() => _isLoading = true);
    try {
      final uri = Uri.parse('http://192.168.100.20:8000/analyze-csv');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'csv_data': text}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (!mounted) return;
        Navigator.push(context, MaterialPageRoute(builder: (_) => ResultsScreen(data: data)));
      } else {
        throw Exception('Server Error: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('CSV Error: $e'), backgroundColor: Colors.red));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Widget _buildCsvTab() {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Enter CSV or JSON data:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.black87)),
              TextButton.icon(
                icon: const Icon(Icons.table_view, size: 16, color: Color(0xFF1B5E20)),
                label: const Text('Sample CSV', style: TextStyle(color: Color(0xFF1B5E20))),
                onPressed: () {
                  _csvController.text = "date,sector,value\n2024-01,Banking,8.5\n2024-02,Banking,7.2\n2024-03,Banking,9.1";
                },
              ),
            ],
          ),
          const SizedBox(height: 8),
          Expanded(
            child: TextField(
              controller: _csvController,
              maxLines: null,
              expands: true,
              textAlignVertical: TextAlignVertical.top,
              decoration: _getInputDecoration('Paste CSV or JSON here...'),
            ),
          ),
          const SizedBox(height: 24),
          _buildAnalyzeButton('Analyze Data', _analyzeCsv),
        ],
      ),
    );
  }

  // --- 7. Real-time Feed ---
  Future<void> _analyzeFeed() async {
    if (_liveFeedItems.isEmpty) return;
    setState(() => _isLoading = true);
    try {
      final uri = Uri.parse('http://192.168.100.20:8000/analyze-multi');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'sources': _liveFeedItems}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (!mounted) return;
        Navigator.push(context, MaterialPageRoute(builder: (_) => ResultsScreen(data: data)));
      } else {
        throw Exception('Server Error: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Feed Error: $e'), backgroundColor: Colors.red));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Widget _buildFeedTab() {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Live Economy Feed', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.black87)),
              Row(
                children: const [
                  SizedBox(width: 12, height: 12, child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFF1B5E20))),
                  SizedBox(width: 8),
                  Text('Updating...', style: TextStyle(color: Colors.grey, fontSize: 12)),
                ],
              )
            ],
          ),
          const SizedBox(height: 16),
          Expanded(
            child: ListView.builder(
              itemCount: _liveFeedItems.length,
              itemBuilder: (context, index) {
                return Container(
                  margin: const EdgeInsets.only(bottom: 12),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4))],
                  ),
                  child: ListTile(
                    contentPadding: const EdgeInsets.all(16),
                    leading: Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(color: Colors.green.shade50, shape: BoxShape.circle),
                      child: const Icon(Icons.article, color: Color(0xFF1B5E20)),
                    ),
                    title: Text(_liveFeedItems[index], style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 24),
          _buildAnalyzeButton('Analyze Feed', _analyzeFeed),
        ],
      ),
    );
  }

  Widget _buildAnalyzeButton(String label, VoidCallback onPressed) {
    return Container(
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [Color(0xFF1B5E20), Color(0xFF00695C)]),
        borderRadius: BorderRadius.circular(16),
        boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 10, offset: Offset(0, 4))],
      ),
      child: ElevatedButton(
        onPressed: _isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.transparent,
          shadowColor: Colors.transparent,
          padding: const EdgeInsets.symmetric(vertical: 20),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        ),
        child: _isLoading
            ? const SizedBox(height: 24, width: 24, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
            : Text(label, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
      ),
    );
  }
}

// -----------------------------------------------------------------------------
// 6. RESULTS SCREEN
// -----------------------------------------------------------------------------
class ResultsScreen extends StatelessWidget {
  final Map<String, dynamic> data;

  const ResultsScreen({super.key, required this.data});

  Color _getRiskColor(int riskScore) {
    if (riskScore <= 3) return Colors.green;
    if (riskScore <= 7) return Colors.orange;
    return Colors.red;
  }

  Color _getPriorityColor(String priority) {
    switch (priority.toUpperCase()) {
      case 'HIGH': return Colors.red;
      case 'MED': return Colors.orange;
      case 'LOW': return Colors.blue;
      default: return Colors.grey;
    }
  }







  Future<void> _executeAction(BuildContext context, Map<String, dynamic> topAction, String eventTitle, int riskScore) async {
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

    await Future.delayed(const Duration(seconds: 3));
    if (context.mounted) Navigator.pop(context);

    final prefs = await SharedPreferences.getInstance();
    List<String> savedActions = prefs.getStringList('executed_actions') ?? [];
    
    final newExecution = {
      'title': eventTitle,
      'subtitle': topAction['description'] ?? 'Action executed successfully.',
      'time': '${DateTime.now().hour}:${DateTime.now().minute.toString().padLeft(2, '0')}',
      'priority': topAction['priority'] ?? 'LOW',
      'risk_score': riskScore.toDouble(),
    };
    
    savedActions.add(jsonEncode(newExecution));
    await prefs.setStringList('executed_actions', savedActions);

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
                Navigator.pop(context); // Pop ResultsScreen
              },
              child: const Text('OK', style: TextStyle(color: Color(0xFF2E7D32))),
            )
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final insights = data['insights'] ?? {};
    final actions = List<Map<String, dynamic>>.from(data['actions'] ?? []);
    final simulation = data['simulation'] ?? {};
    final agentTrace = List<Map<String, dynamic>>.from(data['agent_timeline'] ?? data['agent_trace'] ?? []);
    final actionChain = List<Map<String, dynamic>>.from(data['action_chain'] ?? []);
    final constraints = data['constraints'] ?? {};
    final contradictionAnalysis = data['contradiction_analysis'];
    final temporalAnalysis = data['temporal_analysis'];
    final systemAutonomyScore = data['system_autonomy_score'] ?? 100;
    
    int riskScore = 5;
    if (insights['risk_score'] != null) {
      if (insights['risk_score'] is int) {
        riskScore = insights['risk_score'];
      } else {
        riskScore = int.tryParse(insights['risk_score'].toString()) ?? 5;
      }
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Analysis Results'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(child: _buildAutonomyBadge(systemAutonomyScore)),
            _buildRetryWarnings(agentTrace),

            if (contradictionAnalysis != null && contradictionAnalysis['contradiction_found'] == true)
              _buildContradictionAlert(contradictionAnalysis),
              
            if (temporalAnalysis != null) ...[
              _buildSectionHeader('Temporal Analysis', Icons.timeline),
              _buildTemporalCard(temporalAnalysis),
              const SizedBox(height: 24),
            ],
            
            _buildSectionHeader('Event Insights', Icons.auto_graph),
            _buildInsightsCard(insights, riskScore),
            
            const SizedBox(height: 24),
            _buildSectionHeader('Recommended Actions', Icons.assignment_turned_in),
            ...actions.map((action) => _buildActionCard(action)).toList(),
            const SizedBox(height: 16),
            if (actions.isNotEmpty)
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () => _executeAction(context, actions[0], insights['event'] ?? 'Analysis', riskScore),
                  icon: const Icon(Icons.play_arrow),
                  label: const Text('Execute Top Action', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF2E7D32),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                ),
              ),

            if (actionChain.isNotEmpty) ...[
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
            _buildSectionHeader('Simulation (Top Action)', Icons.science),
            _buildSimulationCard(simulation),

            const SizedBox(height: 24),
            _buildSectionHeader('Antigravity Trace', Icons.terminal),
            _buildTraceCard(agentTrace),
            
            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        children: [
          Icon(icon, color: const Color(0xFF2E7D32), size: 24),
          const SizedBox(width: 8),
          Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Color(0xFF1B5E20))),
        ],
      ),
    );
  }

  Widget _buildInsightsCard(Map<String, dynamic> insights, int riskScore) {
    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Event', style: TextStyle(color: Colors.grey[600], fontSize: 12, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 4),
                      Text(insights['event'] ?? 'N/A', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 16),
                      Text('Sectors Affected', style: TextStyle(color: Colors.grey[600], fontSize: 12, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 4),
                      Wrap(
                        spacing: 8,
                        runSpacing: 4,
                        children: ((insights['sectors'] as List?) ?? []).map((s) => Chip(
                          label: Text(s.toString(), style: const TextStyle(fontSize: 12)),
                          backgroundColor: Colors.green[50],
                          side: BorderSide.none,
                          padding: EdgeInsets.zero,
                        )).toList(),
                      ),
                    ],
                  ),
                ),
                Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: _getRiskColor(riskScore), width: 4),
                  ),
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('$riskScore', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: _getRiskColor(riskScore))),
                        const Text('RISK', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const Divider(height: 32),
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
        ),
      ),
    );
  }

  Widget _buildActionCard(Map<String, dynamic> action) {
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
  }

  Widget _buildSimulationCard(Map<String, dynamic> simulation) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(color: Colors.blue[50], shape: BoxShape.circle),
                  child: const Icon(Icons.people, color: Colors.blue),
                ),
                const SizedBox(width: 12),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Affected Population', style: TextStyle(color: Colors.grey[600], fontSize: 12)),
                    Text('${simulation['affected_count'] ?? 0} individuals', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(color: Colors.amber[50], shape: BoxShape.circle),
                  child: const Icon(Icons.notifications_active, color: Colors.amber),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Notifications Sent', style: TextStyle(color: Colors.grey[600], fontSize: 12)),
                      Text('${simulation['notification_sent'] ?? 0}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                    ],
                  ),
                ),
                if (simulation['dashboard_updated'] == true)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    decoration: BoxDecoration(color: Colors.green[50], borderRadius: BorderRadius.circular(20)),
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.check_circle, color: Color(0xFF2E7D32), size: 16),
                        SizedBox(width: 6),
                        Text('Dashboard Synced', style: TextStyle(color: Color(0xFF2E7D32), fontSize: 12, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(color: Colors.grey[100], borderRadius: BorderRadius.circular(8)),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('BEFORE', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.grey)),
                        const SizedBox(height: 4),
                        Text(simulation['before_state'] ?? 'N/A', style: const TextStyle(fontWeight: FontWeight.w500)),
                      ],
                    ),
                  ),
                ),
                const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 8.0),
                  child: Icon(Icons.arrow_forward, color: Colors.grey),
                ),
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(color: Colors.green[50], borderRadius: BorderRadius.circular(8)),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('AFTER', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.green)),
                        const SizedBox(height: 4),
                        Text(simulation['after_state'] ?? 'N/A', style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2E7D32))),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            if (simulation['email_draft'] != null) ...[
              const Text('Email Communication Draft', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.blueGrey[50],
                  border: Border.all(color: Colors.blueGrey[100]!),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.email, color: Colors.blueGrey, size: 20),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        simulation['email_draft'],
                        style: const TextStyle(fontSize: 13, height: 1.4, color: Colors.black87),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
            ],
            if (simulation['logs'] != null && (simulation['logs'] as List).isNotEmpty) ...[
              const Text('Execution Logs', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E1E1E),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: (simulation['logs'] as List).map<Widget>((log) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 6.0),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('>', style: TextStyle(color: Colors.greenAccent, fontSize: 13, fontFamily: 'monospace')),
                          const SizedBox(width: 8),
                          Expanded(child: Text(log.toString(), style: const TextStyle(color: Colors.greenAccent, fontFamily: 'monospace', fontSize: 12))),
                        ],
                      ),
                    );
                  }).toList(),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }



  Widget _buildTemporalCard(Map<String, dynamic> temporal) {
    final trend = temporal['trend_direction']?.toString().toLowerCase() ?? 'stable';
    Color trendColor = Colors.orange;
    IconData trendIcon = Icons.trending_flat;
    List<double> barHeights = [20, 20, 20, 20, 20];
    
    if (trend == 'rising') {
      trendColor = Colors.red;
      trendIcon = Icons.trending_up;
      barHeights = [10, 15, 25, 35, 50]; // rising risk
    } else if (trend == 'falling') {
      trendColor = Colors.green;
      trendIcon = Icons.trending_down;
      barHeights = [50, 35, 25, 15, 10]; // falling risk
    }

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(trendIcon, color: trendColor, size: 28),
                const SizedBox(width: 8),
                Text('Trend: ${trend.toUpperCase()}', style: TextStyle(color: trendColor, fontWeight: FontWeight.bold, fontSize: 18)),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(color: Colors.blue[50], borderRadius: BorderRadius.circular(8)),
                  child: Text(
                    temporal['percentage_change'] ?? '0%',
                    style: const TextStyle(color: Colors.blue, fontWeight: FontWeight.bold),
                  ),
                )
              ],
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 60,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: barHeights.map((h) => Container(
                  width: 30,
                  height: h,
                  decoration: BoxDecoration(
                    color: trendColor.withOpacity(0.5 + (h / 100)),
                    borderRadius: const BorderRadius.only(topLeft: Radius.circular(4), topRight: Radius.circular(4)),
                  ),
                )).toList(),
              ),
            ),
            const Divider(height: 32),
            const Text('Forecast', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(temporal['forecast'] ?? 'N/A', style: const TextStyle(fontSize: 14)),
            const SizedBox(height: 12),
            const Text('Summary', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(temporal['summary'] ?? 'N/A', style: const TextStyle(fontSize: 14)),
          ],
        ),
      ),
    );
  }


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
  Widget _buildTraceCard(List<Map<String, dynamic>> agentTrace) {
    return Card(
      elevation: 1,
      color: Colors.grey[900],
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: agentTrace.map((trace) {
            if (trace.containsKey('total_time_ms')) {
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Divider(color: Colors.grey),
                  const SizedBox(height: 4),
                  Text('> Total Pipeline Time: ${trace['total_time_ms']} ms', 
                    style: const TextStyle(color: Colors.greenAccent, fontFamily: 'monospace', fontWeight: FontWeight.bold)),
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
  }
}


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
