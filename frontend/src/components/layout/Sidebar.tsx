/**
 * Enhanced Sidebar Component
 * Grouped navigation with sections, icons, and descriptions
 */

import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { NAVIGATION, CHAT_NAVIGATION } from '@/constants/navigation';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { ChevronRight, X } from 'lucide-react';
import { useState } from 'react';

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
  className?: string;
}

export function Sidebar({ isOpen = true, onClose, className }: SidebarProps) {
  const location = useLocation();
  const [expandedSections, setExpandedSections] = useState<string[]>(['core', 'finance', 'intelligence']);

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev =>
      prev.includes(sectionId)
        ? prev.filter(id => id !== sectionId)
        : [...prev, sectionId]
    );
  };

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 z-40 h-screen w-64 border-r bg-background transition-transform duration-300',
        !isOpen && '-translate-x-full lg:translate-x-0',
        className
      )}
    >
      {/* Header */}
      <div className="flex h-16 items-center justify-between border-b px-6">
        <div className="flex items-center space-x-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-blue-600">
            <span className="text-lg font-bold text-white">A</span>
          </div>
          <div>
            <h1 className="text-lg font-bold">AUREXIS AI</h1>
            <p className="text-xs text-muted-foreground">Financial Intelligence</p>
          </div>
        </div>
        {onClose && (
          <Button variant="ghost" size="icon" onClick={onClose} className="lg:hidden">
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      {/* Navigation */}
      <ScrollArea className="h-[calc(100vh-4rem)] px-3 py-4">
        <nav className="space-y-6">
          {NAVIGATION.map((section) => (
            <div key={section.id} className="space-y-1">
              {/* Section Header */}
              <button
                onClick={() => toggleSection(section.id)}
                className="flex w-full items-center justify-between px-3 py-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground hover:text-foreground transition-colors"
              >
                <span>{section.label}</span>
                <ChevronRight
                  className={cn(
                    'h-3 w-3 transition-transform',
                    expandedSections.includes(section.id) && 'rotate-90'
                  )}
                />
              </button>

              {/* Section Items */}
              {expandedSections.includes(section.id) && (
                <div className="space-y-1">
                  {section.items.map((item) => {
                    const Icon = item.icon;
                    const active = isActive(item.path);

                    return (
                      <Link
                        key={item.id}
                        to={item.path}
                        className={cn(
                          'group flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:bg-accent',
                          active && 'bg-accent text-accent-foreground font-medium'
                        )}
                      >
                        <Icon
                          className={cn(
                            'h-4 w-4 shrink-0 transition-colors',
                            active ? 'text-primary' : 'text-muted-foreground group-hover:text-foreground'
                          )}
                        />
                        <div className="flex-1 truncate">
                          <div className="flex items-center justify-between">
                            <span>{item.label}</span>
                            {item.badge && (
                              <Badge variant="secondary" className="ml-auto h-5 px-1.5 text-xs">
                                {item.badge}
                              </Badge>
                            )}
                          </div>
                          {item.description && !active && (
                            <p className="text-xs text-muted-foreground truncate">
                              {item.description}
                            </p>
                          )}
                        </div>
                      </Link>
                    );
                  })}
                </div>
              )}
            </div>
          ))}

          <Separator />

          {/* Chat Assistant (Special) */}
          <div className="space-y-1">
            <Link
              to={CHAT_NAVIGATION.path}
              className={cn(
                'group flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:bg-accent',
                isActive(CHAT_NAVIGATION.path) && 'bg-accent text-accent-foreground font-medium'
              )}
            >
              <CHAT_NAVIGATION.icon
                className={cn(
                  'h-4 w-4 shrink-0 transition-colors',
                  isActive(CHAT_NAVIGATION.path)
                    ? 'text-primary'
                    : 'text-muted-foreground group-hover:text-foreground'
                )}
              />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span>{CHAT_NAVIGATION.label}</span>
                  <Badge variant="default" className="ml-auto h-5 px-1.5 text-xs bg-gradient-to-r from-blue-500 to-purple-500">
                    AI
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground">
                  {CHAT_NAVIGATION.description}
                </p>
              </div>
            </Link>
          </div>
        </nav>

        {/* Footer */}
        <div className="mt-6 px-3 py-4 border-t">
          <div className="text-xs text-muted-foreground space-y-1">
            <p>© 2026 AUREXIS AI</p>
            <p>Version 2.0.0</p>
          </div>
        </div>
      </ScrollArea>
    </aside>
  );
}
