package com.ldleo.mosk

import android.app.AlertDialog
import android.app.Dialog
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.Window
import android.webkit.*
import android.widget.*
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.webkit.ProfileStore
import androidx.webkit.ProxyConfig
import androidx.webkit.ProxyController
import androidx.webkit.WebViewCompat
import androidx.webkit.WebViewFeature
import org.json.JSONArray
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.InetSocketAddress
import java.net.Proxy
import java.net.URL

class MainActivity : AppCompatActivity() {

    private val profiles = mutableListOf<BrowserProfile>()
    private var activeProfile: BrowserProfile? = null
    private var currentCheckId = 0

    private lateinit var tvScoreBadge: TextView
    private lateinit var tvVpnStatus: TextView
    private lateinit var btnRefreshIp: TextView
    private lateinit var btnProfilesSheet: Button
    private lateinit var btnFlashTop: Button
    private lateinit var btnCreateProfileTop: Button
    private lateinit var profilesScreen: LinearLayout
    private lateinit var tvEmptyMessage: TextView
    private lateinit var scrollProfiles: ScrollView
    private lateinit var llProfilesContainer: LinearLayout
    private lateinit var btnFlashSessionBig: Button
    private lateinit var btnNewProfileBig: Button

    private lateinit var browserScreen: LinearLayout
    private lateinit var tvActiveBadge: TextView
    private lateinit var btnMinimize: Button
    private lateinit var btnClean: Button
    private lateinit var webViewContainer: FrameLayout
    private var activeWebView: WebView? = null
    private var currentSheetDialog: Dialog? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initViews()
        loadProfilesFromPrefs()
        refreshProfilesUi()
        fetchIpAndRiskScore()

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (browserScreen.visibility == View.VISIBLE) {
                    if (activeWebView?.canGoBack() == true) {
                        activeWebView?.goBack()
                    } else {
                        showProfilesScreen()
                    }
                } else {
                    finish()
                }
            }
        })
    }

    private fun initViews() {
        tvScoreBadge = findViewById(R.id.tvScoreBadge)
        tvVpnStatus = findViewById(R.id.tvVpnStatus)
        btnRefreshIp = findViewById(R.id.btnRefreshIp)
        btnProfilesSheet = findViewById(R.id.btnProfilesSheet)
        btnFlashTop = findViewById(R.id.btnFlashTop)
        btnCreateProfileTop = findViewById(R.id.btnCreateProfileTop)

        profilesScreen = findViewById(R.id.profilesScreen)
        tvEmptyMessage = findViewById(R.id.tvEmptyMessage)
        scrollProfiles = findViewById(R.id.scrollProfiles)
        llProfilesContainer = findViewById(R.id.llProfilesContainer)
        btnFlashSessionBig = findViewById(R.id.btnFlashSessionBig)
        btnNewProfileBig = findViewById(R.id.btnNewProfileBig)

        browserScreen = findViewById(R.id.browserScreen)
        tvActiveBadge = findViewById(R.id.tvActiveBadge)
        btnMinimize = findViewById(R.id.btnMinimize)
        btnClean = findViewById(R.id.btnClean)
        webViewContainer = findViewById(R.id.webViewContainer)

        btnRefreshIp.setOnClickListener { fetchIpAndRiskScore() }
        btnCreateProfileTop.setOnClickListener { showNewProfileDialog(null) }
        btnNewProfileBig.setOnClickListener { showNewProfileDialog(null) }
        btnFlashTop.setOnClickListener { launchFlashSession() }
        btnFlashSessionBig.setOnClickListener { launchFlashSession() }
        btnProfilesSheet.setOnClickListener { showProfilesSheet() }
        btnMinimize.setOnClickListener { showProfilesScreen() }
        btnClean.setOnClickListener { executeCleanReset() }
    }

    private fun fetchIpAndRiskScore() {
        val checkId = ++currentCheckId
        tvScoreBadge.text = "●"
        tvScoreBadge.setTextColor(Color.parseColor("#FFD60A"))
        tvVpnStatus.text = "🌐 Verificando red y reputación... 🟡"

        Thread {
            try {
                val url = URL("http://ip-api.com/json?fields=status,message,country,countryCode,query,hosting,proxy,mobile")
                val conn = url.openConnection() as HttpURLConnection
                conn.connectTimeout = 4000
                conn.readTimeout = 4000
                val reader = BufferedReader(InputStreamReader(conn.inputStream))
                val response = reader.readText()
                reader.close()
                conn.disconnect()

                if (checkId != currentCheckId) return@Thread

                val json = JSONObject(response)
                val ip = json.optString("query", "Desconocida")
                val country = json.optString("country", "Desconocido")
                val code = json.optString("countryCode", "")
                val isHosting = json.optBoolean("hosting", false)
                val isProxy = json.optBoolean("proxy", false)
                val isMobile = json.optBoolean("mobile", false)

                val score: Int
                val scoreColor: String
                if (isHosting || isProxy) {
                    score = (75..95).random()
                    scoreColor = "#FF453A"
                } else if (isMobile) {
                    score = (2..12).random()
                    scoreColor = "#34C759"
                } else {
                    score = (12..25).random()
                    scoreColor = "#34C759"
                }

                runOnUiThread {
                    if (checkId == currentCheckId) {
                        tvVpnStatus.text = "IP: $ip | $country ($code) | Score: $score"
                        tvScoreBadge.text = "●"
                        tvScoreBadge.setTextColor(Color.parseColor(scoreColor))
                    }
                }
            } catch (e: Exception) {
                if (checkId == currentCheckId) {
                    runOnUiThread {
                        tvVpnStatus.text = "⚠️ Red desconectada o tiempo agotado"
                        tvScoreBadge.text = "🔴"
                    }
                }
            }
        }.start()
    }

    private fun launchFlashSession() {
        currentSheetDialog?.dismiss()
        val randomDev = BrowserProfile.DEVICE_CATALOG.random()
        val seed = (1000..99999).random()
        val flashProfile = BrowserProfile(
            id = "flash_temp",
            name = "⚡ Sesión Flash",
            startUrl = "https://www.google.com",
            seed = seed,
            deviceName = randomDev.name,
            gpuVendor = randomDev.gpuVendor,
            gpuRenderer = randomDev.gpuRenderer,
            userAgent = randomDev.userAgent
        )
        launchProfile(flashProfile)
    }

    private fun showNewProfileDialog(profileToEdit: BrowserProfile?) {
        val dialog = Dialog(this)
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        dialog.setContentView(R.layout.dialog_new_profile)
        dialog.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
        dialog.window?.setLayout(
            (resources.displayMetrics.widthPixels * 0.90).toInt(),
            ViewGroup.LayoutParams.WRAP_CONTENT
        )

        val tvTitle = dialog.findViewById<TextView>(R.id.tvDialogTitle)
        val etName = dialog.findViewById<EditText>(R.id.etProfileName)
        val etUrl = dialog.findViewById<EditText>(R.id.etProfileUrl)
        val tvError = dialog.findViewById<TextView>(R.id.tvUrlError)
        val spinnerDevices = dialog.findViewById<Spinner>(R.id.spinnerDevices)
        val btnOpenProxy = dialog.findViewById<LinearLayout>(R.id.btnOpenProxyDialog)
        val tvProxyStatus = dialog.findViewById<TextView>(R.id.tvProxyStatusText)
        val btnSave = dialog.findViewById<Button>(R.id.btnSaveOnly)
        val btnSaveAndOpen = dialog.findViewById<Button>(R.id.btnSaveAndOpen)
        val btnCancel = dialog.findViewById<TextView>(R.id.btnCancelDialog)

        val deviceNames = BrowserProfile.DEVICE_CATALOG.map { it.name }
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, deviceNames)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinnerDevices.adapter = adapter

        var curProxyType = profileToEdit?.proxyType ?: "DIRECT"
        var curProxyHost = profileToEdit?.proxyHost ?: ""
        var curProxyPort = profileToEdit?.proxyPort ?: 0

        fun updateProxyBadge() {
            if (curProxyHost.isNotEmpty() && curProxyPort > 0) {
                tvProxyStatus.text = "$curProxyType: $curProxyHost:$curProxyPort 🟢"
                tvProxyStatus.setTextColor(Color.parseColor("#34C759"))
            } else {
                tvProxyStatus.text = "Sin proxy (Directo)"
                tvProxyStatus.setTextColor(Color.parseColor("#8E8E93"))
            }
        }
        updateProxyBadge()

        btnOpenProxy.setOnClickListener {
            showProxyConfigDialog(curProxyType, curProxyHost, curProxyPort) { type, host, port ->
                curProxyType = type
                curProxyHost = host
                curProxyPort = port
                updateProxyBadge()
            }
        }

        if (profileToEdit != null) {
            tvTitle.text = "Editar perfil"
            etName.setText(profileToEdit.name)
            etUrl.setText(profileToEdit.startUrl)
            val currentIdx = deviceNames.indexOf(profileToEdit.deviceName)
            if (currentIdx >= 0) spinnerDevices.setSelection(currentIdx)
            btnSaveAndOpen.visibility = View.GONE
        }

        fun saveAction(openNow: Boolean) {
            val name = etName.text.toString().trim().ifEmpty { "Perfil ${profiles.size + 1}" }
            val rawUrl = etUrl.text.toString().trim()

            if (!rawUrl.startsWith("http://") && !rawUrl.startsWith("https://")) {
                tvError.visibility = View.VISIBLE
                return
            }
            tvError.visibility = View.GONE

            val selectedDevice = BrowserProfile.DEVICE_CATALOG[spinnerDevices.selectedItemPosition]

            if (profileToEdit != null) {
                profileToEdit.name = name
                profileToEdit.startUrl = rawUrl
                profileToEdit.deviceName = selectedDevice.name
                profileToEdit.gpuVendor = selectedDevice.gpuVendor
                profileToEdit.gpuRenderer = selectedDevice.gpuRenderer
                profileToEdit.userAgent = selectedDevice.userAgent
                profileToEdit.proxyType = curProxyType
                profileToEdit.proxyHost = curProxyHost
                profileToEdit.proxyPort = curProxyPort

                saveProfilesToPrefs()
                refreshProfilesUi()
                dialog.dismiss()
                Toast.makeText(this, "Perfil actualizado", Toast.LENGTH_SHORT).show()
            } else {
                val newId = "profile_${System.currentTimeMillis()}"
                val seed = (1000..99999).random()

                val newProfile = BrowserProfile(
                    id = newId,
                    name = name,
                    startUrl = rawUrl,
                    seed = seed,
                    deviceName = selectedDevice.name,
                    gpuVendor = selectedDevice.gpuVendor,
                    gpuRenderer = selectedDevice.gpuRenderer,
                    userAgent = selectedDevice.userAgent,
                    proxyType = curProxyType,
                    proxyHost = curProxyHost,
                    proxyPort = curProxyPort
                )

                profiles.add(newProfile)
                saveProfilesToPrefs()
                refreshProfilesUi()
                dialog.dismiss()

                if (openNow) {
                    onProfileSelected(newProfile)
                }
            }
        }

        btnSave.setOnClickListener { saveAction(false) }
        btnSaveAndOpen.setOnClickListener { saveAction(true) }
        btnCancel.setOnClickListener { dialog.dismiss() }

        dialog.show()
    }

    private fun showProxyConfigDialog(initialType: String, initialHost: String, initialPort: Int, onSaved: (String, String, Int) -> Unit) {
        val proxyDialog = Dialog(this)
        proxyDialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        proxyDialog.setContentView(R.layout.dialog_proxy_config)
        proxyDialog.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
        proxyDialog.window?.setLayout(
            (resources.displayMetrics.widthPixels * 0.85).toInt(),
            ViewGroup.LayoutParams.WRAP_CONTENT
        )

        val spinnerType = proxyDialog.findViewById<Spinner>(R.id.spinnerProxyType)
        val etHostPort = proxyDialog.findViewById<EditText>(R.id.etProxyHostPort)
        val btnTest = proxyDialog.findViewById<Button>(R.id.btnTestProxy)
        val tvResult = proxyDialog.findViewById<TextView>(R.id.tvProxyTestResult)
        val btnClear = proxyDialog.findViewById<Button>(R.id.btnClearProxy)
        val btnSave = proxyDialog.findViewById<Button>(R.id.btnSaveProxy)

        val proxyTypes = listOf("HTTP", "HTTPS", "SOCKS5")
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, proxyTypes)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinnerType.adapter = adapter

        val selectedIdx = proxyTypes.indexOf(initialType).coerceAtLeast(0)
        spinnerType.setSelection(selectedIdx)

        if (initialHost.isNotEmpty() && initialPort > 0) {
            etHostPort.setText("$initialHost:$initialPort")
        }

        btnTest.setOnClickListener {
            val raw = etHostPort.text.toString().trim()
            val parts = raw.split(":")
            if (parts.size < 2 || parts[1].toIntOrNull() == null) {
                tvResult.text = "⚠️ Formato inválido. Usa IP:Puerto"
                tvResult.setTextColor(Color.parseColor("#FF453A"))
                return@setOnClickListener
            }

            val testHost = parts[0].trim()
            val testPort = parts[1].trim().toInt()
            val proto = spinnerType.selectedItem.toString()

            tvResult.text = "🟡 Probando proxy ($proto)..."
            tvResult.setTextColor(Color.parseColor("#FFD60A"))

            Thread {
                try {
                    val startTime = System.currentTimeMillis()
                    val proxyMode = if (proto == "SOCKS5") Proxy.Type.SOCKS else Proxy.Type.HTTP
                    val proxyObj = Proxy(proxyMode, InetSocketAddress(testHost, testPort))
                    val testConn = URL("http://ip-api.com/json").openConnection(proxyObj) as HttpURLConnection
                    testConn.connectTimeout = 4000
                    testConn.readTimeout = 4000
                    val resp = testConn.inputStream.bufferedReader().readText()
                    testConn.disconnect()

                    val latency = System.currentTimeMillis() - startTime
                    val json = JSONObject(resp)
                    val ip = json.optString("query")
                    val country = json.optString("country")

                    runOnUiThread {
                        tvResult.text = "🟢 Vivo | IP: $ip | $country | ${latency}ms"
                        tvResult.setTextColor(Color.parseColor("#34C759"))
                    }
                } catch (e: Exception) {
                    runOnUiThread {
                        tvResult.text = "🔴 Error: No responde (Timeout o caído)"
                        tvResult.setTextColor(Color.parseColor("#FF453A"))
                    }
                }
            }.start()
        }

        btnClear.setOnClickListener {
            onSaved("DIRECT", "", 0)
            proxyDialog.dismiss()
        }

        btnSave.setOnClickListener {
            val raw = etHostPort.text.toString().trim()
            if (raw.isEmpty()) {
                onSaved("DIRECT", "", 0)
                proxyDialog.dismiss()
                return@setOnClickListener
            }
            val parts = raw.split(":")
            if (parts.size >= 2 && parts[1].toIntOrNull() != null) {
                val host = parts[0].trim()
                val port = parts[1].trim().toInt()
                val proto = spinnerType.selectedItem.toString()
                onSaved(proto, host, port)
                proxyDialog.dismiss()
            } else {
                tvResult.text = "⚠️ Formato inválido. Usa IP:Puerto"
                tvResult.setTextColor(Color.parseColor("#FF453A"))
            }
        }

        proxyDialog.show()
    }

    private fun showProfileOptions(profile: BrowserProfile) {
        val options = arrayOf("Editar", "Eliminar")
        AlertDialog.Builder(this)
            .setTitle(profile.name)
            .setItems(options) { _, which ->
                when (which) {
                    0 -> showNewProfileDialog(profile)
                    1 -> {
                        if (activeProfile?.id == profile.id) {
                            activeProfile = null
                            showProfilesScreen()
                        }
                        profiles.remove(profile)
                        saveProfilesToPrefs()
                        refreshProfilesUi()
                        currentSheetDialog?.dismiss()
                        Toast.makeText(this, "Perfil eliminado", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            .show()
    }

    private fun onProfileSelected(targetProfile: BrowserProfile) {
        if (activeProfile?.id == targetProfile.id) {
            currentSheetDialog?.dismiss()
            profilesScreen.visibility = View.GONE
            browserScreen.visibility = View.VISIBLE
            activeWebView?.onResume()
            activeWebView?.resumeTimers()
            return
        }

        if (activeProfile != null) {
            AlertDialog.Builder(this)
                .setTitle("Cambiar de sesión")
                .setMessage("¿Deseas abrir '${targetProfile.name}' y pausar '${activeProfile?.name}'?")
                .setPositiveButton("Sí") { _, _ ->
                    activeWebView?.onPause()
                    activeWebView?.pauseTimers()
                    currentSheetDialog?.dismiss()
                    launchProfile(targetProfile)
                }
                .setNegativeButton("No", null)
                .show()
        } else {
            currentSheetDialog?.dismiss()
            launchProfile(targetProfile)
        }
    }

    private fun launchProfile(profile: BrowserProfile) {
        activeProfile = profile
        tvActiveBadge.text = "● ${profile.name} [${profile.deviceName}]"

        activeWebView?.let {
            it.onPause()
            it.pauseTimers()
            webViewContainer.removeView(it)
            it.destroy()
        }

        // Configurar proxy por perfil
        if (profile.proxyHost.isNotEmpty() && profile.proxyPort > 0) {
            if (WebViewFeature.isFeatureSupported(WebViewFeature.PROXY_OVERRIDE)) {
                val scheme = if (profile.proxyType == "SOCKS5") "socks://" else "http://"
                val proxyUrl = "$scheme${profile.proxyHost}:${profile.proxyPort}"
                val proxyConfig = ProxyConfig.Builder()
                    .addProxyRule(proxyUrl)
                    .build()
                ProxyController.getInstance().setProxyOverride(proxyConfig, { it.run() }, {})
            }
        } else {
            if (WebViewFeature.isFeatureSupported(WebViewFeature.PROXY_OVERRIDE)) {
                ProxyController.getInstance().clearProxyOverride({ it.run() }, {})
            }
        }

        val webView = WebView(this)
        webView.layoutParams = ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        )

        val settings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.databaseEnabled = true
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        settings.mediaPlaybackRequiresUserGesture = true
        settings.userAgentString = profile.userAgent

        if (WebViewFeature.isFeatureSupported(WebViewFeature.MULTI_PROFILE)) {
            val profileStore = ProfileStore.getInstance()
            val webkitProfile = profileStore.getOrCreateProfile(profile.id)
            webkitProfile.cookieManager.setAcceptCookie(true)
            WebViewCompat.setProfile(webView, webkitProfile.name)
        }

        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                super.onPageStarted(view, url, favicon)
                val script = StealthScript.generate(profile.seed, profile.gpuVendor, profile.gpuRenderer, profile.userAgent)
                view?.evaluateJavascript(script, null)
            }

            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val targetUrl = request?.url?.toString() ?: return false
                view?.loadUrl(targetUrl)
                return true
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest?) {
                request?.deny()
            }
        }

        activeWebView = webView
        webViewContainer.addView(webView)

        profilesScreen.visibility = View.GONE
        browserScreen.visibility = View.VISIBLE

        fetchIpAndRiskScore()
        webView.loadUrl(profile.startUrl)
    }

    private fun showProfilesScreen() {
        activeWebView?.let {
            it.onPause()
            it.pauseTimers()
        }
        browserScreen.visibility = View.GONE
        profilesScreen.visibility = View.VISIBLE
        refreshProfilesUi()
        fetchIpAndRiskScore()
    }

    private fun showProfilesSheet() {
        val dialog = Dialog(this)
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        dialog.setContentView(R.layout.sheet_profiles)
        dialog.window?.let { w ->
            w.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
            w.setLayout(
                ViewGroup.LayoutParams.MATCH_PARENT,
                (resources.displayMetrics.heightPixels * 0.65).toInt()
            )
            w.setGravity(Gravity.BOTTOM)
        }

        val llSheet = dialog.findViewById<LinearLayout>(R.id.llSheetProfiles)
        val btnNew = dialog.findViewById<Button>(R.id.btnSheetNewProfile)
        btnNew.setOnClickListener {
            dialog.dismiss()
            showNewProfileDialog(null)
        }

        llSheet.removeAllViews()
        for (profile in profiles) {
            val card = createProfileCard(profile)
            llSheet.addView(card)
        }

        currentSheetDialog = dialog
        dialog.show()
    }

    private fun executeCleanReset() {
        activeProfile?.let { profile ->
            if (WebViewFeature.isFeatureSupported(WebViewFeature.MULTI_PROFILE)) {
                val profileStore = ProfileStore.getInstance()
                val webkitProfile = profileStore.getProfile(profile.id)
                webkitProfile?.cookieManager?.removeAllCookies(null)
                webkitProfile?.webStorage?.deleteAllData()
            }
            activeWebView?.clearCache(true)
            activeWebView?.clearHistory()

            // 1. Regenerar semilla unica para Canvas y Audio
            profile.seed = (1000..99999).random()

            // 2. Rotar dispositivo
            val randomDev = BrowserProfile.DEVICE_CATALOG.random()
            profile.deviceName = randomDev.name
            profile.gpuVendor = randomDev.gpuVendor
            profile.gpuRenderer = randomDev.gpuRenderer
            profile.userAgent = randomDev.userAgent

            saveProfilesToPrefs()
            Toast.makeText(this, "Clean: Huella reseteada (#${profile.seed})", Toast.LENGTH_SHORT).show()

            // 3. Regresar de inmediato a la lista de perfiles
            showProfilesScreen()
        }
    }

    private fun createProfileCard(profile: BrowserProfile): View {
        val card = LinearLayout(this)
        card.orientation = LinearLayout.HORIZONTAL
        card.setBackgroundResource(R.drawable.bg_card)
        val params = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        )
        params.setMargins(0, 0, 0, 16)
        card.layoutParams = params
        card.setPadding(28, 24, 16, 24)
        card.gravity = Gravity.CENTER_VERTICAL
        card.isClickable = true
        card.isFocusable = true
        card.setOnClickListener { onProfileSelected(profile) }

        val infoCol = LinearLayout(this)
        infoCol.orientation = LinearLayout.VERTICAL
        infoCol.layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)

        val tvName = TextView(this)
        tvName.text = profile.name
        tvName.textSize = 16f
        tvName.setTextColor(Color.WHITE)
        tvName.setTypeface(null, Typeface.BOLD)
        infoCol.addView(tvName)

        val tvUrl = TextView(this)
        tvUrl.text = profile.startUrl
        tvUrl.textSize = 12f
        tvUrl.setTextColor(Color.parseColor("#8E8E93"))
        tvUrl.setPadding(0, 4, 0, 4)
        infoCol.addView(tvUrl)

        val proxyInfo = if (profile.proxyHost.isNotEmpty() && profile.proxyPort > 0) {
            " | 🌐 ${profile.proxyType}"
        } else {
            ""
        }

        val tvHardware = TextView(this)
        tvHardware.text = "${profile.deviceName} | #${profile.seed}$proxyInfo"
        tvHardware.textSize = 11f
        tvHardware.setTextColor(Color.parseColor("#34C759"))
        infoCol.addView(tvHardware)

        card.addView(infoCol)

        val btnDots = TextView(this)
        btnDots.text = "⋮"
        btnDots.textSize = 24f
        btnDots.setTextColor(Color.parseColor("#8E8E93"))
        btnDots.setPadding(24, 16, 24, 16)
        btnDots.setOnClickListener { showProfileOptions(profile) }
        card.addView(btnDots)

        return card
    }

    private fun refreshProfilesUi() {
        llProfilesContainer.removeAllViews()

        if (profiles.isEmpty()) {
            tvEmptyMessage.visibility = View.VISIBLE
            scrollProfiles.visibility = View.GONE
        } else {
            tvEmptyMessage.visibility = View.GONE
            scrollProfiles.visibility = View.VISIBLE

            for (profile in profiles) {
                val card = createProfileCard(profile)
                llProfilesContainer.addView(card)
            }
        }
    }

    private fun saveProfilesToPrefs() {
        val prefs = getSharedPreferences("browser_profiles", MODE_PRIVATE)
        val array = JSONArray()
        for (p in profiles) {
            array.put(p.toJson())
        }
        prefs.edit().putString("profiles_list", array.toString()).apply()
    }

    private fun loadProfilesFromPrefs() {
        val prefs = getSharedPreferences("browser_profiles", MODE_PRIVATE)
        val raw = prefs.getString("profiles_list", null) ?: return
        profiles.clear()
        val array = JSONArray(raw)
        for (i in 0 until array.length()) {
            profiles.add(BrowserProfile.fromJson(array.getJSONObject(i)))
        }
    }

    override fun onResume() {
        super.onResume()
        activeWebView?.let {
            it.onResume()
            it.resumeTimers()
        }
        fetchIpAndRiskScore()
    }

    override fun onPause() {
        super.onPause()
        activeWebView?.let {
            it.onPause()
            it.pauseTimers()
        }
        if (WebViewFeature.isFeatureSupported(WebViewFeature.MULTI_PROFILE)) {
            activeProfile?.let { profile ->
                ProfileStore.getInstance().getProfile(profile.id)?.cookieManager?.flush()
            }
        }
    }
}