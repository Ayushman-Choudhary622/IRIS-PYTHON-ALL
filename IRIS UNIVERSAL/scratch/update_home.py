with open('app/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Check start and end of main grid columns
start_marker = "{/* ----------------------------------------------------------------------- */}\n        {/* COLUMN 1 (LEFT): Communication, Entertainment & Caretaker App           */}\n        {/* ----------------------------------------------------------------------- */}"
end_marker = "{/* ----------------------------------------------------------------------- */}\n        {/* COLUMN 2 (CENTER): Giant Clock & User's 3D Dynamic Cybernetic IRIS Logo */}"

assert start_marker in code, "Start marker not found"
assert end_marker in code, "End marker not found"

left_idx = code.find(start_marker)
center_idx = code.find(end_marker)

# Also find Right Column start and end
right_marker = "{/* ----------------------------------------------------------------------- */}\n        {/* COLUMN 3 (RIGHT): Emergency (SOS), Health Monitoring & Settings          */}\n        {/* ----------------------------------------------------------------------- */}"
end_of_right_marker = "</div>\n      </div>\n    </div>\n  );\n}"

assert right_marker in code, "Right marker not found"
assert end_of_right_marker in code, "End of right marker not found"

right_idx = code.find(right_marker)
foot_idx = code.find(end_of_right_marker)

new_left_column = """{/* ----------------------------------------------------------------------- */}
        {/* COLUMN 1 (LEFT): 2 Core Tiles (Communication, Caretaker App) + Optional */}
        {/* ----------------------------------------------------------------------- */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 'clamp(10px, 1.6vh, 20px)',
            justifyContent: 'space-between',
            height: '100%',
            minHeight: 0,
          }}
        >
          {/* Core Tile 1: Communication */}
          <Link
            href="/communication"
            onClick={() => {
              if (interfaceSounds) playClickSound((volume / 100) * 0.3);
            }}
            onMouseEnter={() => setHoveredCard('comm')}
            onMouseLeave={() => setHoveredCard(null)}
            style={{
              flex: 1,
              minHeight: 0,
              backgroundColor: hoveredCard === 'comm' ? 'rgba(14, 28, 48, 0.95)' : 'rgba(10, 18, 32, 0.85)',
              border: hoveredCard === 'comm' ? '1.5px solid #38bdf8' : '1.5px solid rgba(56, 189, 248, 0.3)',
              borderRadius: '24px',
              padding: 'clamp(10px, 1.8vh, 26px) clamp(12px, 1.6vw, 24px)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              textAlign: 'center',
              textDecoration: 'none',
              cursor: 'pointer',
              boxShadow: hoveredCard === 'comm'
                ? '0 0 35px rgba(56, 189, 248, 0.65), 0 14px 32px rgba(0, 0, 0, 0.65), inset 0 0 18px rgba(56, 189, 248, 0.22)'
                : '0 0 22px rgba(2, 132, 199, 0.35), 0 8px 22px rgba(0, 0, 0, 0.45), inset 0 0 10px rgba(2, 132, 199, 0.12)',
              transform: hoveredCard === 'comm' ? 'translateY(-3px) scale(1.02)' : 'none',
              transition: 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)',
            }}
          >
            <div
              style={{
                marginBottom: 'clamp(6px, 1vh, 12px)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transform: hoveredCard === 'comm' ? 'scale(1.1)' : 'none',
                transition: 'transform 0.2s ease',
                filter: hoveredCard === 'comm' ? 'drop-shadow(0 0 12px rgba(56, 189, 248, 0.8))' : 'drop-shadow(0 0 6px rgba(255, 255, 255, 0.3))',
              }}
            >
              <svg width="38" height="38" viewBox="0 0 24 24" fill="white">
                <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" />
              </svg>
            </div>
            <span
              style={{
                fontSize: 'clamp(16px, 1.55vw, 22px)',
                fontWeight: 700,
                color: '#ffffff',
                letterSpacing: '-0.01em',
              }}
            >
              Communication
            </span>
          </Link>

          {/* Core Tile 2: Caretaker App */}
          <Link
            href="/care"
            onClick={() => {
              if (interfaceSounds) playClickSound((volume / 100) * 0.3);
            }}
            onMouseEnter={() => setHoveredCard('caretaker')}
            onMouseLeave={() => setHoveredCard(null)}
            style={{
              flex: 1,
              minHeight: 0,
              backgroundColor: hoveredCard === 'caretaker' ? 'rgba(10, 32, 36, 0.95)' : 'rgba(8, 20, 26, 0.85)',
              border: hoveredCard === 'caretaker' ? '1.5px solid #2dd4bf' : '1.5px solid rgba(45, 212, 191, 0.3)',
              borderRadius: '24px',
              padding: 'clamp(10px, 1.8vh, 26px) clamp(12px, 1.6vw, 24px)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              textAlign: 'center',
              textDecoration: 'none',
              cursor: 'pointer',
              boxShadow: hoveredCard === 'caretaker'
                ? '0 0 35px rgba(45, 212, 191, 0.65), 0 14px 32px rgba(0, 0, 0, 0.65), inset 0 0 18px rgba(45, 212, 191, 0.22)'
                : '0 0 22px rgba(13, 148, 136, 0.35), 0 8px 22px rgba(0, 0, 0, 0.45), inset 0 0 10px rgba(13, 148, 136, 0.12)',
              transform: hoveredCard === 'caretaker' ? 'translateY(-3px) scale(1.02)' : 'none',
              transition: 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)',
            }}
          >
            <div
              style={{
                marginBottom: 'clamp(6px, 1vh, 12px)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transform: hoveredCard === 'caretaker' ? 'scale(1.1)' : 'none',
                transition: 'transform 0.2s ease',
                filter: hoveredCard === 'caretaker' ? 'drop-shadow(0 0 12px rgba(45, 212, 191, 0.8))' : 'drop-shadow(0 0 6px rgba(255, 255, 255, 0.3))',
              }}
            >
              <HeartHandshake size={38} strokeWidth={2.4} style={{ color: '#ffffff' }} />
            </div>
            <span
              style={{
                fontSize: 'clamp(16px, 1.55vw, 22px)',
                fontWeight: 700,
                color: '#ffffff',
                letterSpacing: '-0.01em',
              }}
            >
              Caretaker App
            </span>
          </Link>

          {/* Optional Tile on Left: Entertainment (if selected in Settings) */}
          {pinnedHomeTiles.includes('entertainment') && (
            <Link
              href="/entertainment"
              onClick={() => {
                if (interfaceSounds) playClickSound((volume / 100) * 0.3);
              }}
              onMouseEnter={() => setHoveredCard('opt-entertainment')}
              onMouseLeave={() => setHoveredCard(null)}
              style={{
                flex: 1,
                minHeight: 0,
                backgroundColor: hoveredCard === 'opt-entertainment' ? 'rgba(26, 18, 52, 0.95)' : 'rgba(14, 12, 30, 0.85)',
                border: hoveredCard === 'opt-entertainment' ? '1.5px solid #c084fc' : '1.5px solid rgba(192, 132, 252, 0.3)',
                borderRadius: '24px',
                padding: 'clamp(10px, 1.8vh, 26px) clamp(12px, 1.6vw, 24px)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
                textDecoration: 'none',
                cursor: 'pointer',
                boxShadow: hoveredCard === 'opt-entertainment'
                  ? '0 0 35px rgba(192, 132, 252, 0.65), 0 14px 32px rgba(0, 0, 0, 0.65), inset 0 0 18px rgba(192, 132, 252, 0.22)'
                  : '0 0 22px rgba(147, 51, 234, 0.35), 0 8px 22px rgba(0, 0, 0, 0.45), inset 0 0 10px rgba(147, 51, 234, 0.12)',
                transform: hoveredCard === 'opt-entertainment' ? 'translateY(-3px) scale(1.02)' : 'none',
                transition: 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)',
              }}
            >
              <div
                style={{
                  marginBottom: 'clamp(6px, 1vh, 12px)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transform: hoveredCard === 'opt-entertainment' ? 'scale(1.1)' : 'none',
                  transition: 'transform 0.2s ease',
                  filter: hoveredCard === 'opt-entertainment' ? 'drop-shadow(0 0 12px rgba(192, 132, 252, 0.8))' : 'drop-shadow(0 0 6px rgba(255, 255, 255, 0.3))',
                }}
              >
                <svg width="38" height="38" viewBox="0 0 24 24" fill="white">
                  <path d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10 7H8v3H6v-3H3v-2h3V8h2v3h3v2zm4.5 2c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4-3c-.83 0-1.5-.67-1.5-1.5S18.67 9 19.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z" />
                </svg>
              </div>
              <span
                style={{
                  fontSize: 'clamp(16px, 1.55vw, 22px)',
                  fontWeight: 700,
                  color: '#ffffff',
                  letterSpacing: '-0.01em',
                }}
              >
                Entertainment
              </span>
            </Link>
          )}

          {/* Optional Tile on Left: Smart Room IoT (if selected and Left has fewer optional tiles) */}
          {pinnedHomeTiles.includes('iot') && (!pinnedHomeTiles.includes('entertainment') || pinnedHomeTiles.includes('health')) && (
            <Link
              href="/settings"
              onClick={() => {
                if (interfaceSounds) playClickSound((volume / 100) * 0.3);
              }}
              onMouseEnter={() => setHoveredCard('opt-iot')}
              onMouseLeave={() => setHoveredCard(null)}
              style={{
                flex: 1,
                minHeight: 0,
                backgroundColor: hoveredCard === 'opt-iot' ? 'rgba(12, 28, 48, 0.95)' : 'rgba(8, 18, 34, 0.85)',
                border: hoveredCard === 'opt-iot' ? '1.5px solid #38bdf8' : '1.5px solid rgba(56, 189, 248, 0.3)',
                borderRadius: '24px',
                padding: 'clamp(10px, 1.8vh, 26px) clamp(12px, 1.6vw, 24px)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
                textDecoration: 'none',
                cursor: 'pointer',
                boxShadow: hoveredCard === 'opt-iot'
                  ? '0 0 35px rgba(56, 189, 248, 0.65), 0 14px 32px rgba(0, 0, 0, 0.65), inset 0 0 18px rgba(56, 189, 248, 0.22)'
                  : '0 0 22px rgba(56, 189, 248, 0.35), 0 8px 22px rgba(0, 0, 0, 0.45), inset 0 0 10px rgba(56, 189, 248, 0.12)',
                transform: hoveredCard === 'opt-iot' ? 'translateY(-3px) scale(1.02)' : 'none',
                transition: 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)',
              }}
            >
              <div
                style={{
                  marginBottom: 'clamp(6px, 1vh, 12px)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transform: hoveredCard === 'opt-iot' ? 'scale(1.1)' : 'none',
                  transition: 'transform 0.2s ease',
                  filter: hoveredCard === 'opt-iot' ? 'drop-shadow(0 0 12px rgba(56, 189, 248, 0.8))' : 'drop-shadow(0 0 6px rgba(255, 255, 255, 0.3))',
                }}
              >
                <Sun size={38} strokeWidth={2.4} style={{ color: '#ffffff' }} />
              </div>
              <span
                style={{
                  fontSize: 'clamp(16px, 1.55vw, 22px)',
                  fontWeight: 700,
                  color: '#ffffff',
                  letterSpacing: '-0.01em',
                }}
              >
                Smart Room IoT
              </span>
            </Link>
          )}
        </div>
        """

new_right_column = """{/* ----------------------------------------------------------------------- */}
        {/* COLUMN 3 (RIGHT): 2 Core Tiles (Emergency SOS, Settings) + Optional     */}
        {/* ----------------------------------------------------------------------- */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 'clamp(10px, 1.6vh, 20px)',
            justifyContent: 'space-between',
            height: '100%',
            minHeight: 0,
          }}
        >
          {/* Core Tile 3: Emergency / SOS */}
          <button
            onClick={handleEmergencySOS}
            onMouseEnter={() => setHoveredCard('emergency')}
            onMouseLeave={() => setHoveredCard(null)}
            style={{
              flex: 1,
              minHeight: 0,
              width: '100%',
              position: 'relative',
              backgroundColor: hoveredCard === 'emergency' ? 'rgba(38, 12, 18, 0.95)' : 'rgba(24, 8, 12, 0.85)',
              border: hoveredCard === 'emergency' ? '2px solid #f43f5e' : '1.5px solid rgba(244, 63, 94, 0.45)',
              borderRadius: '24px',
              padding: 'clamp(10px, 1.8vh, 26px) clamp(12px, 1.6vw, 24px)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              textAlign: 'center',
              cursor: 'pointer',
              boxShadow: hoveredCard === 'emergency'
                ? '0 0 42px rgba(244, 63, 94, 0.75), 0 14px 32px rgba(0, 0, 0, 0.65), inset 0 0 18px rgba(244, 63, 94, 0.3)'
                : '0 0 24px rgba(225, 29, 72, 0.45), 0 8px 22px rgba(0, 0, 0, 0.45), inset 0 0 10px rgba(225, 29, 72, 0.18)',
              transform: hoveredCard === 'emergency' ? 'translateY(-3px) scale(1.02)' : 'none',
              transition: 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)',
            }}
          >
            {/* SOS Badge Trigger Feedback */}
            {emergencySent && (
              <div
                style={{
                  position: 'absolute',
                  top: '12px',
                  right: '14px',
                  backgroundColor: '#10b981',
                  color: '#ffffff',
                  fontSize: '11px',
                  fontWeight: 800,
                  padding: '4px 8px',
                  borderRadius: '8px',
                  boxShadow: '0 0 12px #10b981',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                }}
              >
                <CheckCircle2 size={12} />
                <span>SENT</span>
              </div>
            )}

            {/* Giant SOS Text Icon */}
            <div
              style={{
                fontSize: 'clamp(32px, 3.8vw, 52px)',
                fontWeight: 900,
                color: '#ffffff',
                lineHeight: 1,
                letterSpacing: '0.04em',
                marginBottom: 'clamp(4px, 0.8vh, 8px)',
                textShadow: '0 0 20px rgba(255, 77, 109, 0.75)',
                transform: hoveredCard === 'emergency' ? 'scale(1.08)' : 'none',
                transition: 'transform 0.2s ease',
              }}
            >
              SOS
            </div>

            <span
              style={{
                fontSize: 'clamp(16px, 1.55vw, 22px)',
                fontWeight: 700,
                color: '#ffffff',
                letterSpacing: '-0.01em',
              }}
            >
              Emergency
            </span>
          </button>

          {/* Optional Tile on Right: Health Monitoring (if selected in Settings) */}
          {pinnedHomeTiles.includes('health') && (
            <Link
              href="/health"
              onClick={() => {
                if (interfaceSounds) playClickSound((volume / 100) * 0.3);
              }}
              onMouseEnter={() => setHoveredCard('opt-health')}
              onMouseLeave={() => setHoveredCard(null)}
              style={{
                flex: 1,
                minHeight: 0,
                backgroundColor: hoveredCard === 'opt-health' ? 'rgba(10, 32, 24, 0.95)' : 'rgba(6, 20, 16, 0.85)',
                border: hoveredCard === 'opt-health' ? '1.5px solid #34d399' : '1.5px solid rgba(52, 211, 153, 0.3)',
                borderRadius: '24px',
                padding: 'clamp(10px, 1.8vh, 26px) clamp(12px, 1.6vw, 24px)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
                textDecoration: 'none',
                cursor: 'pointer',
                boxShadow: hoveredCard === 'opt-health'
                  ? '0 0 35px rgba(52, 211, 153, 0.65), 0 14px 32px rgba(0, 0, 0, 0.65), inset 0 0 18px rgba(52, 211, 153, 0.22)'
                  : '0 0 22px rgba(16, 185, 129, 0.35), 0 8px 22px rgba(0, 0, 0, 0.45), inset 0 0 10px rgba(16, 185, 129, 0.12)',
                transform: hoveredCard === 'opt-health' ? 'translateY(-3px) scale(1.02)' : 'none',
                transition: 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)',
              }}
            >
              <div
                style={{
                  marginBottom: 'clamp(6px, 1vh, 12px)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transform: hoveredCard === 'opt-health' ? 'scale(1.1)' : 'none',
                  transition: 'transform 0.2s ease',
                  filter: hoveredCard === 'opt-health' ? 'drop-shadow(0 0 12px rgba(52, 211, 153, 0.8))' : 'drop-shadow(0 0 6px rgba(255, 255, 255, 0.3))',
                }}
              >
                <Activity size={38} strokeWidth={2.4} style={{ color: '#ffffff' }} />
              </div>
              <span
                style={{
                  fontSize: 'clamp(16px, 1.55vw, 22px)',
                  fontWeight: 700,
                  color: '#ffffff',
                  letterSpacing: '-0.01em',
                }}
              >
                Health Monitoring
              </span>
            </Link>
          )}

          {/* Optional Tile on Right: Smart Room IoT (if selected and Right has fewer optional tiles) */}
          {pinnedHomeTiles.includes('iot') && pinnedHomeTiles.includes('entertainment') && !pinnedHomeTiles.includes('health') && (
            <Link
              href="/settings"
              onClick={() => {
                if (interfaceSounds) playClickSound((volume / 100) * 0.3);
              }}
              onMouseEnter={() => setHoveredCard('opt-r-iot')}
              onMouseLeave={() => setHoveredCard(null)}
              style={{
                flex: 1,
                minHeight: 0,
                backgroundColor: hoveredCard === 'opt-r-iot' ? 'rgba(12, 28, 48, 0.95)' : 'rgba(8, 18, 34, 0.85)',
                border: hoveredCard === 'opt-r-iot' ? '1.5px solid #38bdf8' : '1.5px solid rgba(56, 189, 248, 0.3)',
                borderRadius: '24px',
                padding: 'clamp(10px, 1.8vh, 26px) clamp(12px, 1.6vw, 24px)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
                textDecoration: 'none',
                cursor: 'pointer',
                boxShadow: hoveredCard === 'opt-r-iot'
                  ? '0 0 35px rgba(56, 189, 248, 0.65), 0 14px 32px rgba(0, 0, 0, 0.65), inset 0 0 18px rgba(56, 189, 248, 0.22)'
                  : '0 0 22px rgba(56, 189, 248, 0.35), 0 8px 22px rgba(0, 0, 0, 0.45), inset 0 0 10px rgba(56, 189, 248, 0.12)',
                transform: hoveredCard === 'opt-r-iot' ? 'translateY(-3px) scale(1.02)' : 'none',
                transition: 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)',
              }}
            >
              <div
                style={{
                  marginBottom: 'clamp(6px, 1vh, 12px)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transform: hoveredCard === 'opt-r-iot' ? 'scale(1.1)' : 'none',
                  transition: 'transform 0.2s ease',
                  filter: hoveredCard === 'opt-r-iot' ? 'drop-shadow(0 0 12px rgba(56, 189, 248, 0.8))' : 'drop-shadow(0 0 6px rgba(255, 255, 255, 0.3))',
                }}
              >
                <Sun size={38} strokeWidth={2.4} style={{ color: '#ffffff' }} />
              </div>
              <span
                style={{
                  fontSize: 'clamp(16px, 1.55vw, 22px)',
                  fontWeight: 700,
                  color: '#ffffff',
                  letterSpacing: '-0.01em',
                }}
              >
                Smart Room IoT
              </span>
            </Link>
          )}

          {/* Core Tile 4: Settings */}
          <Link
            href="/settings"
            onClick={() => {
              if (interfaceSounds) playClickSound((volume / 100) * 0.3);
            }}
            onMouseEnter={() => setHoveredCard('settings')}
            onMouseLeave={() => setHoveredCard(null)}
            style={{
              flex: 1,
              minHeight: 0,
              backgroundColor: hoveredCard === 'settings' ? 'rgba(12, 26, 48, 0.95)' : 'rgba(8, 16, 32, 0.85)',
              border: hoveredCard === 'settings' ? '1.5px solid #60a5fa' : '1.5px solid rgba(96, 165, 250, 0.3)',
              borderRadius: '24px',
              padding: 'clamp(10px, 1.8vh, 26px) clamp(12px, 1.6vw, 24px)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              textAlign: 'center',
              textDecoration: 'none',
              cursor: 'pointer',
              boxShadow: hoveredCard === 'settings'
                ? '0 0 35px rgba(96, 165, 250, 0.65), 0 14px 32px rgba(0, 0, 0, 0.65), inset 0 0 18px rgba(96, 165, 250, 0.22)'
                : '0 0 22px rgba(37, 99, 235, 0.35), 0 8px 22px rgba(0, 0, 0, 0.45), inset 0 0 10px rgba(37, 99, 235, 0.12)',
              transform: hoveredCard === 'settings' ? 'translateY(-3px) scale(1.02)' : 'none',
              transition: 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)',
            }}
          >
            <div
              style={{
                marginBottom: 'clamp(6px, 1vh, 12px)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transform: hoveredCard === 'settings' ? 'scale(1.1)' : 'none',
                transition: 'transform 0.2s ease',
                filter: hoveredCard === 'settings' ? 'drop-shadow(0 0 12px rgba(96, 165, 250, 0.8))' : 'drop-shadow(0 0 6px rgba(255, 255, 255, 0.3))',
              }}
            >
              <Settings size={38} strokeWidth={2.4} style={{ color: '#ffffff' }} />
            </div>
            <span
              style={{
                fontSize: 'clamp(16px, 1.55vw, 22px)',
                fontWeight: 700,
                color: '#ffffff',
                letterSpacing: '-0.01em',
              }}
            >
              Settings
            </span>
          </Link>
        </div>
        """

updated_code = code[:left_idx] + new_left_column + code[center_idx:right_idx] + new_right_column + code[foot_idx:]

with open('app/page.tsx', 'w', encoding='utf-8') as out:
    out.write(updated_code)

print("SUCCESS: app/page.tsx updated with 4 default core tiles + optional tiles!")
