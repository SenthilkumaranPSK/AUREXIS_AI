/**
 * Security Page
 * Security settings and account protection
 */

import { PageContainer } from '@/components/layout/PageContainer';
import { StatCard } from '@/components/cards/StatCard';
import { Shield, Lock, Smartphone, Key, AlertTriangle, CheckCircle } from 'lucide-react';

// Mock data
const securityStatus = {
  passwordStrength: 'Strong',
  twoFactorEnabled: true,
  lastPasswordChange: '45 days ago',
  activeSessions: 2,
};

const loginHistory = [
  {
    id: '1',
    device: 'Chrome on Windows',
    location: 'Chennai, India',
    ip: '103.xxx.xxx.xxx',
    date: '2 hours ago',
    status: 'success',
  },
  {
    id: '2',
    device: 'Mobile App on Android',
    location: 'Chennai, India',
    ip: '103.xxx.xxx.xxx',
    date: '1 day ago',
    status: 'success',
  },
  {
    id: '3',
    device: 'Chrome on Windows',
    location: 'Chennai, India',
    ip: '103.xxx.xxx.xxx',
    date: '3 days ago',
    status: 'success',
  },
  {
    id: '4',
    device: 'Safari on iPhone',
    location: 'Mumbai, India',
    ip: '117.xxx.xxx.xxx',
    date: '1 week ago',
    status: 'failed',
  },
];

const activeSessions = [
  {
    id: '1',
    device: 'Chrome on Windows',
    location: 'Chennai, India',
    lastActive: 'Active now',
    current: true,
  },
  {
    id: '2',
    device: 'Mobile App on Android',
    location: 'Chennai, India',
    lastActive: '2 hours ago',
    current: false,
  },
];

export const SecurityPage = () => {
  return (
    <PageContainer
      title="Security"
      subtitle="Manage your account security and privacy settings"
      icon={Shield}
    >
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Password Strength"
          value={securityStatus.passwordStrength}
          trend="neutral"
          icon={Lock}
          color="#10B981"
        />
        <StatCard
          title="2FA Status"
          value={securityStatus.twoFactorEnabled ? 'Enabled' : 'Disabled'}
          trend="neutral"
          icon={Smartphone}
          color={securityStatus.twoFactorEnabled ? '#10B981' : '#EF4444'}
        />
        <StatCard
          title="Last Password Change"
          value={securityStatus.lastPasswordChange}
          trend="neutral"
          icon={Key}
          color="#3B82F6"
        />
        <StatCard
          title="Active Sessions"
          value={securityStatus.activeSessions.toString()}
          trend="neutral"
          icon={Shield}
          color="#8B5CF6"
        />
      </div>

      {/* Security Settings */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Password & Authentication
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                  <Lock className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">Password</p>
                  <p className="text-xs text-gray-500">Last changed 45 days ago</p>
                </div>
              </div>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
                Change
              </button>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                  <Smartphone className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">Two-Factor Authentication</p>
                  <p className="text-xs text-gray-500">Enabled via SMS</p>
                </div>
              </div>
              <button className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium">
                Manage
              </button>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                  <Key className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">Recovery Email</p>
                  <p className="text-xs text-gray-500">sen***@example.com</p>
                </div>
              </div>
              <button className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium">
                Update
              </button>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Security Recommendations
          </h3>
          <div className="space-y-3">
            <div className="flex items-start gap-3 p-3 bg-green-50 border border-green-200 rounded-lg">
              <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-green-900">Strong Password</p>
                <p className="text-xs text-green-700">Your password meets all security requirements</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 bg-green-50 border border-green-200 rounded-lg">
              <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-green-900">2FA Enabled</p>
                <p className="text-xs text-green-700">Your account has two-factor authentication</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 bg-orange-50 border border-orange-200 rounded-lg">
              <AlertTriangle className="w-5 h-5 text-orange-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-orange-900">Password Age</p>
                <p className="text-xs text-orange-700">Consider changing your password (45 days old)</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Active Sessions */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden mb-6">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Active Sessions</h3>
          <p className="text-sm text-gray-500 mt-1">Manage devices with access to your account</p>
        </div>
        <div className="divide-y divide-gray-200">
          {activeSessions.map((session) => (
            <div key={session.id} className="p-6 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <Smartphone className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-900">{session.device}</p>
                    <p className="text-xs text-gray-500">{session.location}</p>
                    <p className="text-xs text-gray-500">{session.lastActive}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  {session.current && (
                    <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                      Current
                    </span>
                  )}
                  {!session.current && (
                    <button className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium">
                      Revoke
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Login History */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Login History</h3>
          <p className="text-sm text-gray-500 mt-1">Recent login attempts to your account</p>
        </div>
        <div className="divide-y divide-gray-200">
          {loginHistory.map((login) => (
            <div key={login.id} className="p-6 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    login.status === 'success' ? 'bg-green-100' : 'bg-red-100'
                  }`}>
                    {login.status === 'success' ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <AlertTriangle className="w-5 h-5 text-red-600" />
                    )}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-900">{login.device}</p>
                    <p className="text-xs text-gray-500">{login.location} • {login.ip}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-900">{login.date}</p>
                  <span className={`text-xs font-medium ${
                    login.status === 'success' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {login.status === 'success' ? 'Successful' : 'Failed'}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </PageContainer>
  );
};
