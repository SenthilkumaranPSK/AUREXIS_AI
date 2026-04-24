/**
 * Profile Page
 * User information and profile management
 */

import { PageContainer } from '@/components/layout/PageContainer';
import { StatCard } from '@/components/cards/StatCard';
import { User, Mail, Phone, MapPin, Briefcase, Calendar, Edit } from 'lucide-react';

// Mock user data
const userData = {
  name: 'Senthilkumaran',
  email: 'senthil@example.com',
  phone: '+91 98765 43210',
  location: 'Chennai, Tamil Nadu',
  occupation: 'Software Engineer',
  company: 'Tech Corp India',
  joinDate: 'January 2024',
  age: 28,
  monthlyIncome: 75000,
  financialGoals: 3,
  activeAlerts: 5,
};

const financialProfile = {
  riskTolerance: 'Moderate',
  investmentHorizon: 'Long-term (10+ years)',
  primaryGoal: 'Wealth Accumulation',
  secondaryGoals: ['Emergency Fund', 'Car Purchase', 'Retirement'],
};

const preferences = {
  currency: 'INR (₹)',
  language: 'English',
  timezone: 'Asia/Kolkata (IST)',
  dateFormat: 'DD/MM/YYYY',
};

export const ProfilePage = () => {
  return (
    <PageContainer
      title="Profile"
      subtitle="Manage your personal information and preferences"
      icon={User}
      action={
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          <Edit className="w-4 h-4" />
          Edit Profile
        </button>
      }
    >
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Member Since"
          value={userData.joinDate}
          trend="neutral"
          icon={Calendar}
          color="#3B82F6"
        />
        <StatCard
          title="Monthly Income"
          value={`₹${userData.monthlyIncome.toLocaleString()}`}
          trend="neutral"
          icon={Briefcase}
          color="#10B981"
        />
        <StatCard
          title="Active Goals"
          value={userData.financialGoals.toString()}
          trend="neutral"
          icon={User}
          color="#8B5CF6"
        />
        <StatCard
          title="Active Alerts"
          value={userData.activeAlerts.toString()}
          trend="neutral"
          icon={Mail}
          color="#F59E0B"
        />
      </div>

      {/* Personal Information */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Personal Information
          </h3>
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                <User className="w-6 h-6 text-blue-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-500">Full Name</p>
                <p className="text-base font-semibold text-gray-900">{userData.name}</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
                <Mail className="w-6 h-6 text-green-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-500">Email Address</p>
                <p className="text-base font-semibold text-gray-900">{userData.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0">
                <Phone className="w-6 h-6 text-purple-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-500">Phone Number</p>
                <p className="text-base font-semibold text-gray-900">{userData.phone}</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center flex-shrink-0">
                <MapPin className="w-6 h-6 text-orange-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-500">Location</p>
                <p className="text-base font-semibold text-gray-900">{userData.location}</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                <Briefcase className="w-6 h-6 text-blue-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-500">Occupation</p>
                <p className="text-base font-semibold text-gray-900">
                  {userData.occupation} at {userData.company}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Quick Stats
          </h3>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500 mb-1">Age</p>
              <p className="text-2xl font-bold text-gray-900">{userData.age} years</p>
            </div>
            <div>
              <p className="text-sm text-gray-500 mb-1">Account Status</p>
              <span className="inline-block px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                Active
              </span>
            </div>
            <div>
              <p className="text-sm text-gray-500 mb-1">Verification</p>
              <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                Verified
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Financial Profile */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Financial Profile
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Risk Tolerance</span>
              <span className="text-sm font-semibold text-gray-900">{financialProfile.riskTolerance}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Investment Horizon</span>
              <span className="text-sm font-semibold text-gray-900">{financialProfile.investmentHorizon}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Primary Goal</span>
              <span className="text-sm font-semibold text-gray-900">{financialProfile.primaryGoal}</span>
            </div>
            <div className="py-2">
              <span className="text-sm text-gray-600 block mb-2">Secondary Goals</span>
              <div className="flex flex-wrap gap-2">
                {financialProfile.secondaryGoals.map((goal, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium"
                  >
                    {goal}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Preferences
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Currency</span>
              <span className="text-sm font-semibold text-gray-900">{preferences.currency}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Language</span>
              <span className="text-sm font-semibold text-gray-900">{preferences.language}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Timezone</span>
              <span className="text-sm font-semibold text-gray-900">{preferences.timezone}</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-sm text-gray-600">Date Format</span>
              <span className="text-sm font-semibold text-gray-900">{preferences.dateFormat}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-5">
        <h4 className="font-semibold text-blue-900 mb-3">Profile Actions</h4>
        <div className="flex flex-wrap gap-3">
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
            Update Information
          </button>
          <button className="px-4 py-2 bg-white border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors text-sm font-medium">
            Change Password
          </button>
          <button className="px-4 py-2 bg-white border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors text-sm font-medium">
            Export Data
          </button>
        </div>
      </div>
    </PageContainer>
  );
};
