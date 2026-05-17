import os

filepath = r"d:\humaa\EconoSense-pk\econosense_app\lib\main.dart"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update TabController length
content = content.replace(
    "_tabController = TabController(length: 4, vsync: this);",
    "_tabController = TabController(length: 6, vsync: this);"
)

# 2. Update Tabs
old_tabs = """          tabs: const [
            Tab(icon: Icon(Icons.text_fields), text: 'Text'),
            Tab(icon: Icon(Icons.link), text: 'URL'),
            Tab(icon: Icon(Icons.picture_as_pdf), text: 'PDF'),
            Tab(icon: Icon(Icons.library_books), text: 'Multi-Source'),
          ],"""
new_tabs = """          tabs: const [
            Tab(icon: Icon(Icons.text_fields), text: 'Text'),
            Tab(icon: Icon(Icons.link), text: 'URL'),
            Tab(icon: Icon(Icons.picture_as_pdf), text: 'PDF'),
            Tab(icon: Icon(Icons.library_books), text: 'Multi-Source'),
            Tab(icon: Icon(Icons.table_chart), text: 'CSV/JSON'),
            Tab(icon: Icon(Icons.feed), text: 'Feed'),
          ],"""
content = content.replace(old_tabs, new_tabs)

# 3. Update TabBarView children
old_tab_children = """      body: TabBarView(
        controller: _tabController,
        children: [
          _buildTextTab(),
          _buildUrlTab(),
          _buildPdfTab(),
          _buildMultiSourceTab(),
        ],
      ),"""
new_tab_children = """      body: TabBarView(
        controller: _tabController,
        children: [
          _buildTextTab(),
          _buildUrlTab(),
          _buildPdfTab(),
          _buildMultiSourceTab(),
          _buildCsvTab(),
          _buildFeedTab(),
        ],
      ),"""
content = content.replace(old_tab_children, new_tab_children)

# 4. Add new controllers and Multi-Source functions
old_controllers = """  final TextEditingController _urlController = TextEditingController();
  final TextEditingController _source1Controller = TextEditingController();
  final TextEditingController _source2Controller = TextEditingController();
  final TextEditingController _source3Controller = TextEditingController();
  bool _isLoading = false;"""
new_controllers = """  final TextEditingController _urlController = TextEditingController();
  final TextEditingController _source1Controller = TextEditingController();
  final TextEditingController _source2Controller = TextEditingController();
  final TextEditingController _source3Controller = TextEditingController();
  final TextEditingController _csvController = TextEditingController();
  Timer? _feedTimer;
  List<String> _liveFeedItems = [
    "State Bank of Pakistan announces new monetary policy, increasing interest rates by 100 bps.",
    "FBR reports a 15% increase in tax revenue collection for the current fiscal quarter.",
    "IMF approves the next tranche of the bailout package for Pakistan."
  ];
  final List<String> _possibleHeadlines = [
    "PSX gains 500 points amid positive investor sentiment.",
    "Textile exports decline by 5% due to high energy costs.",
    "Government announces new subsidy for the agriculture sector.",
    "Foreign exchange reserves increase by \$50 million.",
    "Inflation rate drops to 24% in the latest monthly report.",
    "New trade agreement signed with regional partners."
  ];
  bool _isLoading = false;"""
content = content.replace(old_controllers, new_controllers)

# Add Feed Timer to initState
old_init = """  void initState() {
    super.initState();
    _tabController = TabController(length: 6, vsync: this);
  }"""
new_init = """  void initState() {
    super.initState();
    _tabController = TabController(length: 6, vsync: this);
    _feedTimer = Timer.periodic(const Duration(seconds: 30), (timer) {
      if (mounted) {
        setState(() {
          _liveFeedItems.insert(0, _possibleHeadlines[DateTime.now().second % _possibleHeadlines.length]);
          if (_liveFeedItems.length > 5) {
            _liveFeedItems.removeLast();
          }
        });
      }
    });
  }"""
content = content.replace(old_init, new_init)

old_dispose = """    _tabController.dispose();
    _textController.dispose();
    _urlController.dispose();
    _source1Controller.dispose();
    _source2Controller.dispose();
    _source3Controller.dispose();
    super.dispose();"""
new_dispose = """    _tabController.dispose();
    _textController.dispose();
    _urlController.dispose();
    _source1Controller.dispose();
    _source2Controller.dispose();
    _source3Controller.dispose();
    _csvController.dispose();
    _feedTimer?.cancel();
    super.dispose();"""
content = content.replace(old_dispose, new_dispose)

new_methods = """
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
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Enter CSV or JSON data:', style: TextStyle(fontWeight: FontWeight.bold)),
              TextButton.icon(
                icon: const Icon(Icons.table_view, size: 16),
                label: const Text('Sample CSV'),
                onPressed: () {
                  _csvController.text = "date,sector,value\\n2024-01,Banking,8.5\\n2024-02,Banking,7.2\\n2024-03,Banking,9.1";
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
              decoration: const InputDecoration(
                hintText: 'Paste CSV or JSON here...',
              ),
            ),
          ),
          const SizedBox(height: 16),
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
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Live Economy Feed', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              Row(
                children: const [
                  SizedBox(width: 12, height: 12, child: CircularProgressIndicator(strokeWidth: 2)),
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
                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    leading: const Icon(Icons.article, color: Colors.blue),
                    title: Text(_liveFeedItems[index], style: const TextStyle(fontSize: 14)),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 16),
          _buildAnalyzeButton('Analyze Feed', _analyzeFeed),
        ],
      ),
    );
  }
"""
content = content.replace("  Widget _buildAnalyzeButton(String label, VoidCallback onPressed) {", new_methods + "\n  Widget _buildAnalyzeButton(String label, VoidCallback onPressed) {")

# 5. Update ResultsScreen build method
old_results_vars = """    final actionChain = List<Map<String, dynamic>>.from(data['action_chain'] ?? []);
    final constraints = data['constraints'] ?? {};
    final contradictionAnalysis = data['contradiction_analysis'];"""
new_results_vars = """    final actionChain = List<Map<String, dynamic>>.from(data['action_chain'] ?? []);
    final constraints = data['constraints'] ?? {};
    final contradictionAnalysis = data['contradiction_analysis'];
    final temporalAnalysis = data['temporal_analysis'];"""
content = content.replace(old_results_vars, new_results_vars)


old_results_body = """            if (contradictionAnalysis != null && contradictionAnalysis['contradiction_found'] == true)
              _buildContradictionAlert(contradictionAnalysis),
            
            _buildSectionHeader('Event Insights', Icons.auto_graph),"""
new_results_body = """            if (contradictionAnalysis != null && contradictionAnalysis['contradiction_found'] == true)
              _buildContradictionAlert(contradictionAnalysis),
              
            if (temporalAnalysis != null) ...[
              _buildSectionHeader('Temporal Analysis', Icons.timeline),
              _buildTemporalCard(temporalAnalysis),
              const SizedBox(height: 24),
            ],
            
            _buildSectionHeader('Event Insights', Icons.auto_graph),"""
content = content.replace(old_results_body, new_results_body)


# 6. Add Temporal Widget
temporal_widget = """
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
"""

content = content.replace("  Widget _buildContradictionAlert(Map<String, dynamic> contradiction) {", temporal_widget + "\n  Widget _buildContradictionAlert(Map<String, dynamic> contradiction) {")

# 7. Replace trace formatting
old_trace = """            return Padding(
              padding: const EdgeInsets.only(bottom: 8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('> ${trace['agent']}...', style: TextStyle(color: Colors.grey[400], fontFamily: 'monospace', fontSize: 13)),
                  Text('${trace['time_ms']} ms', style: const TextStyle(color: Colors.white, fontFamily: 'monospace', fontSize: 13)),
                ],
              ),
            );"""
new_trace = """            return Padding(
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
            );"""
content = content.replace(old_trace, new_trace)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Dart file updated successfully.")
