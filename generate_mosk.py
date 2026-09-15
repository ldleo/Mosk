import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("app/src/main/java/com/ldleo/mosk", exist_ok=True)
os.makedirs("app/src/main/res/layout", exist_ok=True)
os.makedirs("app/src/main/res/values", exist_ok=True)
os.makedirs("app/src/main/res/drawable", exist_ok=True)

sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192
}

for folder, size in sizes.items():
    os.makedirs(f"app/src/main/res/{folder}", exist_ok=True)
    font = None
    for fpath in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ):
        if os.path.exists(fpath):
            font = ImageFont.truetype(fpath, int(size * 0.23))
            break
    if not font:
        font = ImageFont.load_default()

    text = "MOSK"
    box = (2, 2, size - 3, size - 3)

    # Adaptive / Square Icon
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(box, radius=size // 4, fill=(18, 18, 18, 255), outline=(50, 50, 50, 255), width=max(1, size // 48))
    b0, b1, b2, b3 = draw.textbbox((0, 0), text, font=font)
    w, h = b2 - b0, b3 - b1
    x = (size - w) / 2
    y = (size - h) / 2 - b1
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    img.save(f"app/src/main/res/{folder}/ic_launcher.png")

    # Round Icon
    rimg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(rimg)
    rdraw.ellipse(box, fill=(14, 14, 14, 255), outline=(60, 60, 60, 255), width=max(1, size // 48))
    rdraw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    rimg.save(f"app/src/main/res/{folder}/ic_launcher_round.png")

with open("settings.gradle", "w") as f:
    f.write("""pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "Mosk"
include ':app'
""")

with open("build.gradle", "w") as f:
    f.write("""plugins {
    id 'com.android.application' version '8.2.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.22' apply false
}
""")

with open("app/build.gradle", "w") as f:
    f.write("""plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.ldleo.mosk'
    compileSdk 34

    defaultConfig {
        applicationId "com.ldleo.mosk"
        minSdk 26
        targetSdk 34
        versionCode 1
        versionName "2.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = '17'
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.webkit:webkit:1.12.1'
}
""")

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:label="Mosk"
        android:supportsRtl="true"
        android:theme="@style/Theme.Mosk"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:configChanges="orientation|screenSize|keyboardHidden"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>""")

with open("app/src/main/res/values/strings.xml", "w") as f:
    f.write("""<resources>
    <string name="app_name">Mosk</string>
</resources>""")

with open("app/src/main/res/values/colors.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="bg_black">#0D0D0D</color>
    <color name="card_dark">#181818</color>
    <color name="card_border">#2A2A2A</color>
    <color name="text_primary">#F0F0F0</color>
    <color name="text_secondary">#8E8E93</color>
    <color name="accent_purple">#C5B3F9</color>
    <color name="accent_green">#34C759</color>
    <color name="accent_red">#FF453A</color>
    <color name="accent_yellow">#FFD60A</color>
</resources>""")

with open("app/src/main/res/values/themes.xml", "w") as f:
    f.write("""<resources>
    <style name="Theme.Mosk" parent="Theme.Material3.Dark.NoActionBar">
        <item name="android:statusBarColor">@color/bg_black</item>
        <item name="android:navigationBarColor">@color/bg_black</item>
    </style>
</resources>""")

with open("app/src/main/res/drawable/bg_card.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/card_dark" />
    <corners android:radius="14dp" />
    <stroke android:width="1dp" android:color="@color/card_border" />
</shape>""")

with open("app/src/main/res/drawable/bg_input.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#242424" />
    <corners android:radius="10dp" />
    <stroke android:width="1dp" android:color="#383838" />
</shape>""")

with open("app/src/main/res/drawable/bg_sheet.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#141414" />
    <corners android:topLeftRadius="20dp" android:topRightRadius="20dp" />
    <stroke android:width="1dp" android:color="#2C2C2C" />
</shape>""")

with open("app/src/main/res/layout/activity_main.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="@color/bg_black">

    <LinearLayout
        android:id="@+id/ipBanner"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:background="#121212"
        android:padding="8dp"
        android:gravity="center_vertical">

        <TextView
            android:id="@+id/tvScoreBadge"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="●"
            android:textColor="@color/accent_yellow"
            android:textSize="14sp"
            android:paddingEnd="6dp" />

        <TextView
            android:id="@+id/tvVpnStatus"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="🌐 Verificando red y reputación..."
            android:textColor="@color/text_secondary"
            android:textSize="12sp" />

        <TextView
            android:id="@+id/btnRefreshIp"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="🔄"
            android:padding="4dp"
            android:textSize="14sp" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/topBar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="10dp"
        android:background="@color/card_dark"
        android:gravity="center_vertical">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Mosk"
            android:textColor="@color/text_primary"
            android:textSize="18sp"
            android:textStyle="bold" />

        <View
            android:layout_width="0dp"
            android:layout_height="1dp"
            android:layout_weight="1" />

        <Button
            android:id="@+id/btnProfilesSheet"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:text="Perfiles"
            android:textSize="12sp"
            android:backgroundTint="#2C2C2E"
            android:textColor="@color/text_primary" />

        <Button
            android:id="@+id/btnFlashTop"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:text="⚡ Flash"
            android:textSize="12sp"
            android:layout_marginStart="6dp"
            android:backgroundTint="#F5A623"
            android:textColor="#000000" />

        <Button
            android:id="@+id/btnCreateProfileTop"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:text="+ Nuevo"
            android:textSize="12sp"
            android:layout_marginStart="6dp"
            android:backgroundTint="@color/accent_purple"
            android:textColor="#000000" />
    </LinearLayout>

    <FrameLayout
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1">

        <LinearLayout
            android:id="@+id/profilesScreen"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical"
            android:gravity="center"
            android:padding="16dp">

            <TextView
                android:id="@+id/tvEmptyMessage"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Sin perfiles todavía"
                android:textColor="@color/text_secondary"
                android:textSize="18sp"
                android:layout_marginBottom="24dp" />

            <ScrollView
                android:id="@+id/scrollProfiles"
                android:layout_width="match_parent"
                android:layout_height="0dp"
                android:layout_weight="1"
                android:visibility="gone">
                <LinearLayout
                    android:id="@+id/llProfilesContainer"
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical" />
            </ScrollView>

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal">

                <Button
                    android:id="@+id/btnFlashSessionBig"
                    android:layout_width="0dp"
                    android:layout_height="50dp"
                    android:layout_weight="1"
                    android:text="⚡ Sesión Flash"
                    android:textColor="#000000"
                    android:textStyle="bold"
                    android:backgroundTint="#F5A623"
                    android:layout_marginEnd="6dp" />

                <Button
                    android:id="@+id/btnNewProfileBig"
                    android:layout_width="0dp"
                    android:layout_height="50dp"
                    android:layout_weight="1"
                    android:text="+ Nuevo perfil"
                    android:textColor="#000000"
                    android:textStyle="bold"
                    android:backgroundTint="@color/accent_purple" />
            </LinearLayout>
        </LinearLayout>

        <LinearLayout
            android:id="@+id/browserScreen"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical"
            android:visibility="gone">

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:padding="8dp"
                android:background="#151515"
                android:gravity="center_vertical">

                <TextView
                    android:id="@+id/tvActiveBadge"
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="Perfil Activo"
                    android:textColor="@color/accent_green"
                    android:textSize="12sp" />

                <Button
                    android:id="@+id/btnMinimize"
                    android:layout_width="wrap_content"
                    android:layout_height="32dp"
                    android:text="Minimizar"
                    android:textSize="11sp"
                    android:backgroundTint="#2C2C2E"
                    android:textColor="@color/text_primary"
                    android:layout_marginEnd="6dp" />

                <Button
                    android:id="@+id/btnClean"
                    android:layout_width="wrap_content"
                    android:layout_height="32dp"
                    android:text="Clean"
                    android:textSize="11sp"
                    android:backgroundTint="@color/accent_red"
                    android:textColor="@color/text_primary" />
            </LinearLayout>

            <FrameLayout
                android:id="@+id/webViewContainer"
                android:layout_width="match_parent"
                android:layout_height="match_parent" />
        </LinearLayout>
    </FrameLayout>
</LinearLayout>""")

with open("app/src/main/res/layout/dialog_new_profile.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="20dp"
    android:background="@drawable/bg_card">

    <TextView
        android:id="@+id/tvDialogTitle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Nuevo perfil"
        android:textColor="@color/text_primary"
        android:textSize="18sp"
        android:textStyle="bold"
        android:layout_marginBottom="14dp" />

    <EditText
        android:id="@+id/etProfileName"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:hint="Nombre del perfil (ej. Banco PT)"
        android:textColor="@color/text_primary"
        android:textColorHint="@color/text_secondary"
        android:background="@drawable/bg_input"
        android:padding="12dp"
        android:layout_marginBottom="12dp"
        android:textSize="14sp" />

    <EditText
        android:id="@+id/etProfileUrl"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:hint="URL del sitio (https://...)"
        android:textColor="@color/text_primary"
        android:textColorHint="@color/text_secondary"
        android:background="@drawable/bg_input"
        android:padding="12dp"
        android:textSize="14sp"
        android:inputType="textUri" />

    <TextView
        android:id="@+id/tvUrlError"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="⚠️ URL inválida (incluye http:// o https://)"
        android:textColor="@color/accent_red"
        android:textSize="12sp"
        android:paddingTop="4dp"
        android:paddingBottom="4dp"
        android:visibility="gone" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Modelo de Dispositivo:"
        android:textColor="@color/text_secondary"
        android:textSize="12sp"
        android:layout_marginTop="10dp"
        android:layout_marginBottom="4dp" />

    <Spinner
        android:id="@+id/spinnerDevices"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:background="@drawable/bg_input"
        android:padding="8dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Proxy (opcional):"
        android:textColor="@color/text_secondary"
        android:textSize="12sp"
        android:layout_marginTop="12dp"
        android:layout_marginBottom="4dp" />

    <LinearLayout
        android:id="@+id/btnOpenProxyDialog"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:orientation="horizontal"
        android:background="@drawable/bg_input"
        android:padding="12dp"
        android:gravity="center_vertical"
        android:Clickable="true"
        android:focusable="true">

        <TextView
            android:id="@+id/tvProxyStatusText"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Sin proxy (Directo)"
            android:textColor="@color/text_secondary"
            android:textSize="13sp" />

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="⚙️"
            android:textSize="14sp" />
    </LinearLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:layout_marginTop="18dp">

        <Button
            android:id="@+id/btnSaveOnly"
            android:layout_width="0dp"
            android:layout_height="44dp"
            android:layout_weight="1"
            android:text="Guardar perfil"
            android:textSize="12sp"
            android:backgroundTint="#2C2C2E"
            android:textColor="@color/text_primary"
            android:layout_marginEnd="6dp" />

        <Button
            android:id="@+id/btnSaveAndOpen"
            android:layout_width="0dp"
            android:layout_height="44dp"
            android:layout_weight="1"
            android:text="Guardar y abrir"
            android:textSize="12sp"
            android:backgroundTint="@color/accent_purple"
            android:textColor="#000000" />
    </LinearLayout>

    <TextView
        android:id="@+id/btnCancelDialog"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="CANCELAR"
        android:textColor="@color/text_secondary"
        android:gravity="center"
        android:padding="12dp"
        android:textSize="13sp"
        android:textStyle="bold" />
</LinearLayout>""")

with open("app/src/main/res/layout/dialog_proxy_config.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="20dp"
    android:background="@drawable/bg_card">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Configurar Proxy"
        android:textColor="@color/text_primary"
        android:textSize="18sp"
        android:textStyle="bold"
        android:layout_marginBottom="14dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Protocolo:"
        android:textColor="@color/text_secondary"
        android:textSize="12sp"
        android:layout_marginBottom="4dp" />

    <Spinner
        android:id="@+id/spinnerProxyType"
        android:layout_width="match_parent"
        android:layout_height="44dp"
        android:background="@drawable/bg_input"
        android:padding="8dp"
        android:layout_marginBottom="12dp" />

    <EditText
        android:id="@+id/etProxyHostPort"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:hint="IP:Puerto (ej. 185.220.101.5:8080)"
        android:textColor="@color/text_primary"
        android:textColorHint="@color/text_secondary"
        android:background="@drawable/bg_input"
        android:padding="12dp"
        android:layout_marginBottom="10dp"
        android:textSize="14sp" />

    <Button
        android:id="@+id/btnTestProxy"
        android:layout_width="match_parent"
        android:layout_height="40dp"
        android:text="🧪 Probar Proxy"
        android:textSize="12sp"
        android:backgroundTint="#2C2C2E"
        android:textColor="@color/text_primary" />

    <TextView
        android:id="@+id/tvProxyTestResult"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text=""
        android:textSize="12sp"
        android:paddingTop="6dp"
        android:paddingBottom="6dp" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:layout_marginTop="12dp">

        <Button
            android:id="@+id/btnClearProxy"
            android:layout_width="0dp"
            android:layout_height="44dp"
            android:layout_weight="1"
            android:text="Quitar proxy"
            android:textSize="12sp"
            android:backgroundTint="#2C2C2E"
            android:textColor="@color/accent_red"
            android:layout_marginEnd="6dp" />

        <Button
            android:id="@+id/btnSaveProxy"
            android:layout_width="0dp"
            android:layout_height="44dp"
            android:layout_weight="1"
            android:text="Guardar"
            android:textSize="12sp"
            android:backgroundTint="@color/accent_purple"
            android:textColor="#000000" />
    </LinearLayout>
</LinearLayout>""")

with open("app/src/main/res/layout/sheet_profiles.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="16dp"
    android:background="@drawable/bg_sheet">

    <View
        android:layout_width="40dp"
        android:layout_height="4dp"
        android:background="#444444"
        android:layout_gravity="center_horizontal"
        android:layout_marginBottom="12dp" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:layout_marginBottom="12dp">

        <TextView
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Mis Perfiles (Mosk)"
            android:textColor="@color/text_primary"
            android:textSize="18sp"
            android:textStyle="bold" />

        <Button
            android:id="@+id/btnSheetNewProfile"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:text="+ Nuevo"
            android:textSize="12sp"
            android:backgroundTint="@color/accent_purple"
            android:textColor="#000000" />
    </LinearLayout>

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="320dp">
        <LinearLayout
            android:id="@+id/llSheetProfiles"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical" />
    </ScrollView>
</LinearLayout>""")

with open("app/src/main/java/com/ldleo/mosk/StealthScript.kt", "w") as f:
    f.write('''package com.ldleo.mosk

object StealthScript {
    fun generate(seed: Int, vendor: String, renderer: String, userAgent: String): String {
        return """
        (function() {
            try {
                const seed = $seed;

                // 1. WebRTC Shield (Apagado completo de fugas IP)
                window.RTCPeerConnection = undefined;
                window.webkitRTCPeerConnection = undefined;

                // 2. Hardware Specs coherentes
                Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8, configurable: false });
                Object.defineProperty(navigator, 'deviceMemory', { get: () => 8, configurable: false });
                Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 5, configurable: false });
                Object.defineProperty(navigator, 'platform', { get: () => 'Linux aarch64', configurable: false });

                // 3. WebGL Spoofing (Vendor y Renderer exactos)
                const fakeVendor = "$vendor";
                const fakeRenderer = "$renderer";

                function patchWebGL(proto) {
                    if (!proto) return;
                    const origGetParameter = proto.getParameter;
                    proto.getParameter = function(parameter) {
                        if (parameter === 37445) return fakeVendor;
                        if (parameter === 37446) return fakeRenderer;
                        return origGetParameter.apply(this, arguments);
                    };
                }
                patchWebGL(window.WebGLRenderingContext ? window.WebGLRenderingContext.prototype : null);
                patchWebGL(window.WebGL2RenderingContext ? window.WebGL2RenderingContext.prototype : null);

                // 4. Canvas Noise Injection (Firma matematica unica por Seed)
                const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function() {
                    const ctx = this.getContext('2d');
                    if (ctx && this.width > 0 && this.height > 0) {
                        try {
                            const imgData = ctx.getImageData(0, 0, Math.min(this.width, 10), Math.min(this.height, 10));
                            for (let i = 0; i < imgData.data.length; i += 4) {
                                imgData.data[i] = (imgData.data[i] + (seed % 9) + 1) % 256;
                            }
                            ctx.putImageData(imgData, 0, 0);
                        } catch(e) {}
                    }
                    return origToDataURL.apply(this, arguments);
                };

                const origGetImageData = CanvasRenderingContext2D.prototype.getImageData;
                CanvasRenderingContext2D.prototype.getImageData = function() {
                    const res = origGetImageData.apply(this, arguments);
                    if (res && res.data && res.data.length > 0) {
                        for (let i = 0; i < Math.min(res.data.length, 60); i += 4) {
                            res.data[i] = (res.data[i] + (seed % 9) + 1) % 256;
                        }
                    }
                    return res;
                };

                // 5. AudioContext Noise Injection
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (AudioCtx) {
                    const origGetChannelData = AudioBuffer.prototype.getChannelData;
                    AudioBuffer.prototype.getChannelData = function(channel) {
                        const buffer = origGetChannelData.apply(this, arguments);
                        for (let i = 0; i < Math.min(buffer.length, 30); i++) {
                            buffer[i] = buffer[i] + ((seed % 7) * 0.000001);
                        }
                        return buffer;
                    };
                }

                // 6. Camouflage [native code]
                const nativeToString = Function.prototype.toString;
                const customToString = function() {
                    if (this === HTMLCanvasElement.prototype.toDataURL) {
                        return "function toDataURL() { [native code] }";
                    }
                    if (this === CanvasRenderingContext2D.prototype.getImageData) {
                        return "function getImageData() { [native code] }";
                    }
                    return nativeToString.apply(this, arguments);
                };
                Object.defineProperty(Function.prototype, 'toString', {
                    value: customToString,
                    configurable: false,
                    writable: false
                });
            } catch(e) {}
        })();
        """.trimIndent()
    }
}''')

with open("app/src/main/java/com/ldleo/mosk/ProfileModel.kt", "w") as f:
    f.write("""package com.ldleo.mosk

import org.json.JSONObject

data class DevicePreset(
    val name: String,
    val modelCode: String,
    val gpuVendor: String,
    val gpuRenderer: String,
    val userAgent: String
)

data class BrowserProfile(
    val id: String,
    var name: String,
    var startUrl: String,
    var seed: Int,
    var deviceName: String,
    var gpuVendor: String,
    var gpuRenderer: String,
    var userAgent: String,
    var proxyType: String = "DIRECT",
    var proxyHost: String = "",
    var proxyPort: Int = 0
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("id", id)
        json.put("name", name)
        json.put("startUrl", startUrl)
        json.put("seed", seed)
        json.put("deviceName", deviceName)
        json.put("gpuVendor", gpuVendor)
        json.put("gpuRenderer", gpuRenderer)
        json.put("userAgent", userAgent)
        json.put("proxyType", proxyType)
        json.put("proxyHost", proxyHost)
        json.put("proxyPort", proxyPort)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): BrowserProfile {
            return BrowserProfile(
                id = json.getString("id"),
                name = json.getString("name"),
                startUrl = json.getString("startUrl"),
                seed = json.getInt("seed"),
                deviceName = json.optString("deviceName", "Samsung Galaxy S24 Ultra"),
                gpuVendor = json.getString("gpuVendor"),
                gpuRenderer = json.getString("gpuRenderer"),
                userAgent = json.optString("userAgent", "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"),
                proxyType = json.optString("proxyType", "DIRECT"),
                proxyHost = json.optString("proxyHost", ""),
                proxyPort = json.optInt("proxyPort", 0)
            )
        }

        // 6 Modelos Optimizados y Coherentes (Gama Media, Media-Alta y Alta)
        val DEVICE_CATALOG = listOf(
            DevicePreset("Samsung Galaxy S24 Ultra", "SM-S928B", "Qualcomm", "Adreno (TM) 750", "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Xiaomi POCO F6", "24069PC21G", "Qualcomm", "Adreno (TM) 735", "Mozilla/5.0 (Linux; Android 14; 24069PC21G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Google Pixel 8 Pro", "Pixel 8 Pro", "ARM", "Mali-G715", "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Samsung Galaxy S23", "SM-S911B", "Qualcomm", "Adreno (TM) 740", "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Xiaomi 14", "23127PN0CG", "Qualcomm", "Adreno (TM) 750", "Mozilla/5.0 (Linux; Android 14; 23127PN0CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Motorola Edge 50 Pro", "motorola edge 50 pro", "Qualcomm", "Adreno (TM) 720", "Mozilla/5.0 (Linux; Android 14; motorola edge 50 pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36")
        )
    }
}""")

with open("app/src/main/java/com/ldleo/mosk/MainActivity.kt", "w") as f:
    f.write("""package com.ldleo.mosk

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
}""")
