import React from "react";
import { Link, useLocation } from "react-router-dom";

const Sidebar: React.FC = () => {
  const location = useLocation();

  const navigation = [
    { name: "Dashboard", href: "/", icon: "📊" },
    { name: "Transactions", href: "/transactions", icon: "💳" },
    { name: "Budgets", href: "/budgets", icon: "🎯" },
    { name: "Insights", href: "/insights", icon: "🔍" },
    { name: "Chat", href: "/chat", icon: "🤖" },
  ];

  return (
    <div className="w-64 bg-white shadow-sm min-h-screen">
      <nav className="mt-8">
        <div className="px-4 space-y-2">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className={`flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                location.pathname === item.href
                  ? "bg-blue-100 text-blue-700"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              }`}
            >
              <span className="mr-3">{item.icon}</span>
              {item.name}
            </Link>
          ))}
        </div>
      </nav>
    </div>
  );
};

export default Sidebar;
