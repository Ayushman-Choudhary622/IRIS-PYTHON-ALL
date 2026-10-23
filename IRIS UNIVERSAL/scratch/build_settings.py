import sys

with open('scratch_settings_restored.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Lucide icon imports
old_icons = """import {
  Home,
  Sliders,
  Monitor,
  Volume2,
  Shield,
  Cpu,
  Accessibility,
  Check,
  RotateCcw,
  Bell,
  Sparkles,
  Download,
  Wifi,
  ChevronRight,
  Flame,
  Info,
  type LucideIcon,
} from 'lucide-react';"""

new_icons = """import {
  Home,
  Sliders,
  Monitor,
  Volume2,
  Shield,
  Cpu,
  Accessibility,
  Check,
  RotateCcw,
  Bell,
  Sparkles,
  Download,
  Wifi,
  ChevronRight,
  Flame,
  Info,
  LayoutGrid,
  Gamepad2,
  Activity,
  Sun,
  Lightbulb,
  Fan,
  Wind,
  ExternalLink,
  CheckCircle2,
  type LucideIcon,
} from 'lucide-react';"""

if old_icons not in content:
    print('Error: old_icons block not found')
    sys.exit(1)
content = content.replace(old_icons, new_icons, 1)

# 2. Add 'tiles' to TABS at the beginning
old_tabs = """const TABS: TabConfig[] = [
  {
    id: 'accessibility',"""

new_tabs = """const TABS: TabConfig[] = [
  {
    id: 'tiles',
    label: 'HOMESCREEN & APPS',
    icon: LayoutGrid,
    color: '#ec4899',
    accent: 'rgba(236, 72, 153, 0.45)',
    desc: 'Entertainment, Health, Smart IoT & homescreen tiles',
  },
  {
    id: 'accessibility',"""

if old_tabs not in content:
    print('Error: old_tabs block not found')
    sys.exit(1)
content = content.replace(old_tabs, new_tabs, 1)

# 3. Update useIrisSettings destructuring to include pinnedHomeTiles and IoT states
old_settings_hook = """  const {
    uiScale,
    reducedMotion,
    highContrast,
    largeControls,
    focusMode,
    showVirtualCursor,
    invertX,
    invertY,
    ntfyTopic,
    theme,
    hudDensity,
    showFps,
    interfaceSounds,
    volume,
    tts,
    speechRate,
    graphicsQuality,
    targetFps,
    showTelemetry,
    setSetting,
    resetSettings,
    exportSettings,
  } = useIrisSettings();"""

new_settings_hook = """  const {
    uiScale,
    reducedMotion,
    highContrast,
    largeControls,
    focusMode,
    showVirtualCursor,
    invertX,
    invertY,
    ntfyTopic,
    theme,
    hudDensity,
    showFps,
    interfaceSounds,
    volume,
    tts,
    speechRate,
    graphicsQuality,
    targetFps,
    showTelemetry,
    pinnedHomeTiles = [],
    iotBedroomLight = false,
    iotCeilingFan = true,
    iotBedsideLamp = false,
    iotRoomAc = true,
    setSetting,
    resetSettings,
    exportSettings,
  } = useIrisSettings();

  const togglePinnedTile = (tileId: string) => {
    handleClickSound();
    const current = pinnedHomeTiles || [];
    const exists = current.includes(tileId);
    const updated = exists ? current.filter((id) => id !== tileId) : [...current, tileId];
    setSetting('pinnedHomeTiles', updated);
    showToast(exists ? 'Removed tile from Homescreen' : '✓ Added tile to Homescreen!');
  };"""

if old_settings_hook not in content:
    print('Error: old_settings_hook block not found')
    sys.exit(1)
content = content.replace(old_settings_hook, new_settings_hook, 1)

# 4. Insert activeTab === 'tiles' rendering before activeTab === 'accessibility'
old_panel_content = """          {/* Module Content */}
          <div style={{ flex: 1, overflowY: 'auto', paddingRight: '4px' }}>
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.15 }}
              >
                {/* 1. ACCESSIBILITY */}
                {activeTab === 'accessibility' && ("""

tiles_jsx = """          {/* Module Content */}
          <div style={{ flex: 1, overflowY: 'auto', paddingRight: '4px' }}>
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.15 }}
              >
                {/* 0. HOMESCREEN TILES & APPS */}
                {activeTab === 'tiles' && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    {/* Status Overview Card */}
                    <div
                      style={{
                        backgroundColor: 'rgba(15, 23, 42, 0.75)',
                        border: '1.5px solid rgba(236, 72, 153, 0.35)',
                        borderRadius: '20px',
                        padding: '18px 22px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        boxShadow: '0 0 25px rgba(236, 72, 153, 0.15)',
                      }}
                    >
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                          <CheckCircle2 size={18} color="#ec4899" />
                          <span style={{ fontSize: '14px', fontWeight: 900, color: '#ffffff', letterSpacing: '0.04em' }}>
                            HOMESCREEN CONFIGURATION
                          </span>
                        </div>
                        <p style={{ fontSize: '12px', color: '#94a3b8', margin: 0, lineHeight: 1.5 }}>
                          Default main screen has <strong>4 core tiles</strong> (Communication, Caretaker App, SOS, Settings).
                          Toggle any of the 3 tiles below to optionally add them to your Homescreen.
                        </p>
                      </div>

                      <span
                        style={{
                          backgroundColor: pinnedHomeTiles.length === 0 ? 'rgba(56, 189, 248, 0.15)' : 'rgba(236, 72, 153, 0.2)',
                          border: pinnedHomeTiles.length === 0 ? '1px solid #38bdf8' : '1px solid #ec4899',
                          color: pinnedHomeTiles.length === 0 ? '#38bdf8' : '#ec4899',
                          fontSize: '11px',
                          fontWeight: 800,
                          padding: '6px 14px',
                          borderRadius: '12px',
                          fontFamily: "'JetBrains Mono', monospace",
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {pinnedHomeTiles.length === 0
                          ? 'DEFAULT 4 TILES ACTIVE'
                          : `${pinnedHomeTiles.length} OPTIONAL TILE(S) ADDED (${4 + pinnedHomeTiles.length} TILES TOTAL)`}
                      </span>
                    </div>

                    {/* The 3 Tiles Section */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                      {/* Tile 1: Entertainment */}
                      <div
                        style={{
                          backgroundColor: 'rgba(15, 23, 42, 0.85)',
                          border: pinnedHomeTiles.includes('entertainment')
                            ? '2px solid #c084fc'
                            : '1.5px solid rgba(192, 132, 252, 0.3)',
                          borderRadius: '20px',
                          padding: '18px 22px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          boxShadow: pinnedHomeTiles.includes('entertainment')
                            ? '0 0 25px rgba(192, 132, 252, 0.25)'
                            : 'none',
                          transition: 'all 0.2s ease',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                          <div
                            style={{
                              width: '48px',
                              height: '48px',
                              borderRadius: '14px',
                              backgroundColor: 'rgba(192, 132, 252, 0.18)',
                              border: '1.5px solid #c084fc',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              color: '#c084fc',
                              flexShrink: 0,
                            }}
                          >
                            <Gamepad2 size={26} />
                          </div>
                          <div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                              <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#ffffff', margin: 0 }}>
                                Entertainment
                              </h3>
                              {pinnedHomeTiles.includes('entertainment') && (
                                <span
                                  style={{
                                    fontSize: '10px',
                                    fontWeight: 800,
                                    backgroundColor: 'rgba(192, 132, 252, 0.2)',
                                    color: '#c084fc',
                                    padding: '2px 8px',
                                    borderRadius: '6px',
                                    border: '1px solid #c084fc44',
                                  }}
                                >
                                  ON HOMESCREEN
                                </span>
                              )}
                            </div>
                            <p style={{ fontSize: '12px', color: '#94a3b8', margin: '3px 0 0 0' }}>
                              Gaze-driven arcade games, binaural lo-fi music therapy & audiobooks
                            </p>
                          </div>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <Link
                            href="/entertainment"
                            onClick={handleClickSound}
                            style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '6px',
                              backgroundColor: 'rgba(192, 132, 252, 0.15)',
                              border: '1.5px solid #c084fc',
                              borderRadius: '12px',
                              padding: '8px 16px',
                              color: '#c084fc',
                              fontSize: '12px',
                              fontWeight: 800,
                              textDecoration: 'none',
                              cursor: 'pointer',
                              transition: 'all 0.15s ease',
                            }}
                          >
                            <span>Open</span>
                            <ExternalLink size={14} />
                          </Link>

                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', paddingLeft: '8px', borderLeft: '1px solid rgba(255,255,255,0.1)' }}>
                            <span style={{ fontSize: '11px', color: '#cbd5e1', fontWeight: 700 }}>Show on Home:</span>
                            <CyberToggle
                              checked={pinnedHomeTiles.includes('entertainment')}
                              onChange={() => togglePinnedTile('entertainment')}
                              color="#c084fc"
                            />
                          </div>
                        </div>
                      </div>

                      {/* Tile 2: Health Monitoring */}
                      <div
                        style={{
                          backgroundColor: 'rgba(15, 23, 42, 0.85)',
                          border: pinnedHomeTiles.includes('health')
                            ? '2px solid #34d399'
                            : '1.5px solid rgba(52, 211, 153, 0.3)',
                          borderRadius: '20px',
                          padding: '18px 22px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          boxShadow: pinnedHomeTiles.includes('health')
                            ? '0 0 25px rgba(52, 211, 153, 0.25)'
                            : 'none',
                          transition: 'all 0.2s ease',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                          <div
                            style={{
                              width: '48px',
                              height: '48px',
                              borderRadius: '14px',
                              backgroundColor: 'rgba(52, 211, 153, 0.18)',
                              border: '1.5px solid #34d399',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              color: '#34d399',
                              flexShrink: 0,
                            }}
                          >
                            <Activity size={26} />
                          </div>
                          <div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                              <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#ffffff', margin: 0 }}>
                                Health Monitoring
                              </h3>
                              {pinnedHomeTiles.includes('health') && (
                                <span
                                  style={{
                                    fontSize: '10px',
                                    fontWeight: 800,
                                    backgroundColor: 'rgba(52, 211, 153, 0.2)',
                                    color: '#34d399',
                                    padding: '2px 8px',
                                    borderRadius: '6px',
                                    border: '1px solid #34d39944',
                                  }}
                                >
                                  ON HOMESCREEN
                                </span>
                              )}
                            </div>
                            <p style={{ fontSize: '12px', color: '#94a3b8', margin: '3px 0 0 0' }}>
                              Timeline of logged symptoms, pain severity scores, medication requests & caregiver response timestamps
                            </p>
                          </div>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <Link
                            href="/health"
                            onClick={handleClickSound}
                            style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '6px',
                              backgroundColor: 'rgba(52, 211, 153, 0.15)',
                              border: '1.5px solid #34d399',
                              borderRadius: '12px',
                              padding: '8px 16px',
                              color: '#34d399',
                              fontSize: '12px',
                              fontWeight: 800,
                              textDecoration: 'none',
                              cursor: 'pointer',
                              transition: 'all 0.15s ease',
                            }}
                          >
                            <span>Open</span>
                            <ExternalLink size={14} />
                          </Link>

                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', paddingLeft: '8px', borderLeft: '1px solid rgba(255,255,255,0.1)' }}>
                            <span style={{ fontSize: '11px', color: '#cbd5e1', fontWeight: 700 }}>Show on Home:</span>
                            <CyberToggle
                              checked={pinnedHomeTiles.includes('health')}
                              onChange={() => togglePinnedTile('health')}
                              color="#34d399"
                            />
                          </div>
                        </div>
                      </div>

                      {/* Tile 3: Smart Room IoT */}
                      <div
                        style={{
                          backgroundColor: 'rgba(15, 23, 42, 0.85)',
                          border: pinnedHomeTiles.includes('iot')
                            ? '2px solid #38bdf8'
                            : '1.5px solid rgba(56, 189, 248, 0.3)',
                          borderRadius: '20px',
                          padding: '18px 22px',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '14px',
                          boxShadow: pinnedHomeTiles.includes('iot')
                            ? '0 0 25px rgba(56, 189, 248, 0.25)'
                            : 'none',
                          transition: 'all 0.2s ease',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                            <div
                              style={{
                                width: '48px',
                                height: '48px',
                                borderRadius: '14px',
                                backgroundColor: 'rgba(56, 189, 248, 0.18)',
                                border: '1.5px solid #38bdf8',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: '#38bdf8',
                                flexShrink: 0,
                              }}
                            >
                              <Sun size={26} />
                            </div>
                            <div>
                              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#ffffff', margin: 0 }}>
                                  Smart Room IoT
                                </h3>
                                {pinnedHomeTiles.includes('iot') && (
                                  <span
                                    style={{
                                      fontSize: '10px',
                                      fontWeight: 800,
                                      backgroundColor: 'rgba(56, 189, 248, 0.2)',
                                      color: '#38bdf8',
                                      padding: '2px 8px',
                                      borderRadius: '6px',
                                      border: '1px solid #38bdf844',
                                    }}
                                  >
                                    ON HOMESCREEN
                                  </span>
                                )}
                              </div>
                              <p style={{ fontSize: '12px', color: '#94a3b8', margin: '3px 0 0 0' }}>
                                Environmental controls for patient bedroom lighting, ceiling fan, bedside lamp, and room AC
                              </p>
                            </div>
                          </div>

                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span style={{ fontSize: '11px', color: '#cbd5e1', fontWeight: 700 }}>Show on Home:</span>
                            <CyberToggle
                              checked={pinnedHomeTiles.includes('iot')}
                              onChange={() => togglePinnedTile('iot')}
                              color="#38bdf8"
                            />
                          </div>
                        </div>

                        {/* Interactive In-Settings IoT Relays */}
                        <div
                          style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(4, 1fr)',
                            gap: '10px',
                            paddingTop: '10px',
                            borderTop: '1px solid rgba(255, 255, 255, 0.08)',
                          }}
                        >
                          {[
                            { key: 'iotBedroomLight', label: 'Bedroom Light', state: iotBedroomLight, color: '#f59e0b', icon: Lightbulb },
                            { key: 'iotCeilingFan', label: 'Ceiling Fan', state: iotCeilingFan, color: '#38bdf8', icon: Fan },
                            { key: 'iotBedsideLamp', label: 'Bedside Lamp', state: iotBedsideLamp, color: '#fbbf24', icon: Sun },
                            { key: 'iotRoomAc', label: 'Room AC', state: iotRoomAc, color: '#34d399', icon: Wind },
                          ].map((item) => {
                            const IconComponent = item.icon;
                            return (
                              <button
                                key={item.key}
                                type="button"
                                onClick={() => {
                                  handleClickSound();
                                  setSetting(item.key as any, !item.state);
                                }}
                                style={{
                                  backgroundColor: item.state ? 'rgba(15, 23, 42, 0.95)' : 'rgba(10, 16, 28, 0.7)',
                                  border: item.state ? `1.5px solid ${item.color}` : '1px solid rgba(255, 255, 255, 0.1)',
                                  borderRadius: '14px',
                                  padding: '12px 10px',
                                  display: 'flex',
                                  flexDirection: 'column',
                                  alignItems: 'center',
                                  justifyContent: 'center',
                                  gap: '8px',
                                  cursor: 'pointer',
                                  boxShadow: item.state ? `0 0 16px ${item.color}33` : 'none',
                                  transition: 'all 0.18s ease',
                                }}
                              >
                                <IconComponent size={20} color={item.state ? item.color : '#64748b'} />
                                <span style={{ fontSize: '11px', fontWeight: 700, color: '#ffffff' }}>
                                  {item.label}
                                </span>
                                <span
                                  style={{
                                    fontSize: '9px',
                                    fontWeight: 900,
                                    fontFamily: "'JetBrains Mono', monospace",
                                    color: item.state ? item.color : '#64748b',
                                  }}
                                >
                                  {item.state ? 'ON' : 'OFF'}
                                </span>
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* 1. ACCESSIBILITY */}
                {activeTab === 'accessibility' && ("""

if old_panel_content not in content:
    print('Error: old_panel_content block not found')
    sys.exit(1)
content = content.replace(old_panel_content, tiles_jsx, 1)

with open('app/settings/page.tsx', 'w', encoding='utf-8') as out:
    out.write(content)

print('SUCCESS: app/settings/page.tsx updated!')
