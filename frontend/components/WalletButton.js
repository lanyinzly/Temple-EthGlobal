import { useAccount, useConnect, useDisconnect } from 'wagmi'
import { useState } from 'react'

export default function WalletButton() {
  const { address, isConnected } = useAccount()
  const { connect, connectors } = useConnect()
  const { disconnect } = useDisconnect()
  const [showConnectors, setShowConnectors] = useState(false)

  const formatAddress = (addr) => {
    if (!addr) return ''
    return `${addr.slice(0, 6)}...${addr.slice(-4)}`
  }

  if (isConnected) {
    return (
      <div style={{ position: 'relative' }}>
        <button 
          className="header-btn"
          onClick={() => setShowConnectors(!showConnectors)}
          style={{ backgroundColor: '#28a745', color: 'white' }}
        >
          {formatAddress(address)}
        </button>
        {showConnectors && (
          <div style={{
            position: 'absolute',
            top: '100%',
            right: 0,
            backgroundColor: 'white',
            border: '1px solid #ddd',
            borderRadius: '8px',
            padding: '10px',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
            zIndex: 1000,
            minWidth: '150px'
          }}>
            <div style={{ 
              fontSize: '12px', 
              color: '#666', 
              marginBottom: '10px',
              wordBreak: 'break-all'
            }}>
              {address}
            </div>
            <button
              onClick={() => {
                disconnect()
                setShowConnectors(false)
              }}
              style={{
                width: '100%',
                padding: '8px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '12px',
                cursor: 'pointer'
              }}
            >
              断开连接
            </button>
          </div>
        )}
      </div>
    )
  }

  return (
    <div style={{ position: 'relative' }}>
      <button 
        className="header-btn"
        onClick={() => setShowConnectors(!showConnectors)}
      >
        连接钱包
      </button>
      {showConnectors && (
        <div style={{
          position: 'absolute',
          top: '100%',
          right: 0,
          backgroundColor: 'white',
          border: '1px solid #ddd',
          borderRadius: '8px',
          padding: '10px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
          zIndex: 1000,
          minWidth: '150px'
        }}>
          {connectors.map((connector) => (
            <button
              key={connector.id}
              onClick={() => {
                connect({ connector })
                setShowConnectors(false)
              }}
              style={{
                width: '100%',
                padding: '8px',
                marginBottom: '5px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '12px',
                cursor: 'pointer'
              }}
            >
              {connector.name}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}