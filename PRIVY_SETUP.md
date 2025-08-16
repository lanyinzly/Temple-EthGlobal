# Privy Integration Setup Guide

## Overview
Your Temple application now uses Privy for wallet authentication and payments. Privy provides a better user experience with:
- Email + wallet login options
- Embedded wallets for users without crypto wallets
- Social login support
- Better mobile experience
- Simplified onboarding

## Setup Steps

### 1. Get Privy App ID
1. Go to [Privy Dashboard](https://dashboard.privy.io)
2. Create a new app or use existing one
3. Copy your App ID

### 2. Configure Environment Variables
Create `.env.local` file in your frontend directory:

```bash
# Privy Configuration
NEXT_PUBLIC_PRIVY_APP_ID=your-privy-app-id-here

# Payment Addresses (optional, can be set in code)
NEXT_PUBLIC_PAYMENT_ETH_ADDRESS=your-eth-address-here
NEXT_PUBLIC_PAYMENT_SOL_ADDRESS=your-sol-address-here
NEXT_PUBLIC_PAYMENT_APT_ADDRESS=your-apt-address-here
```

### 3. Configure Privy Settings
In your Privy dashboard:
- Set allowed domains (localhost:3000 for development)
- Configure login methods (email, wallet, social)
- Set up embedded wallet options
- Configure appearance/branding

## What Changed

### Components Updated:
- **WalletProvider.js**: Now uses Privy instead of pure wagmi
- **WalletButton.js**: Simplified login/logout with Privy
- **PaymentHandler.js**: Uses Privy wallet for transactions

### New Features:
- **Email Login**: Users can sign up with email and get embedded wallet
- **Social Login**: Support for Google, Twitter, etc. (configure in Privy dashboard)
- **Better UX**: Simplified wallet connection process
- **Mobile Friendly**: Better mobile wallet experience

### Payment Flow:
1. User clicks "Connect Wallet" → Privy login modal opens
2. User can choose: Email signup, Connect existing wallet, or Social login
3. After authentication, wallet address is available for payments
4. Payment process remains the same (ETH transactions)

## Benefits of Privy Integration

### For Users:
- **Easier Onboarding**: Can start with email, no need to install MetaMask first
- **Embedded Wallets**: Privy creates wallets for email users automatically
- **Social Login**: Connect with Google, Twitter, etc.
- **Mobile Friendly**: Better mobile experience

### For Developers:
- **Simplified Code**: Less wallet connection logic needed
- **Better Analytics**: User authentication and wallet usage analytics
- **Cross-Platform**: Works consistently across devices
- **Security**: Privy handles wallet security and key management

## Testing

1. **Development**: 
   ```bash
   npm run dev
   ```
   Visit http://localhost:3000

2. **Try Different Login Methods**:
   - Email signup (creates embedded wallet)
   - Connect existing MetaMask wallet
   - Social login (if configured)

3. **Test Payment Flow**:
   - Go through divination process
   - Reach payment page (suangua5)
   - Connect wallet via Privy
   - Complete ETH payment

## Production Deployment

1. Add production domain to Privy dashboard
2. Set production environment variables
3. Test wallet connections and payments on production
4. Monitor payments and user analytics in Privy dashboard

## Support

- **Privy Docs**: https://docs.privy.io
- **Privy Discord**: https://discord.gg/privy
- **Code Issues**: Check console for errors, Privy provides detailed error messages

Your Temple app now has enterprise-grade wallet authentication with Privy! 🚀