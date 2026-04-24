/**
 * Page Container Component
 * Consistent page wrapper with title, description, and actions
 */

import { ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { ArrowLeft, LucideIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface PageContainerProps {
  title: string;
  description?: string;
  subtitle?: string; // Alias for description
  children: ReactNode;
  actions?: ReactNode;
  action?: ReactNode; // Alias for actions
  showBack?: boolean;
  className?: string;
  icon?: LucideIcon; // Optional icon
}

export function PageContainer({
  title,
  description,
  subtitle,
  children,
  actions,
  action,
  showBack = false,
  className,
  icon: Icon,
}: PageContainerProps) {
  const navigate = useNavigate();
  
  // Use subtitle as fallback for description
  const displayDescription = description || subtitle;
  // Use action as fallback for actions
  const displayActions = actions || action;

  return (
    <div className={cn('flex flex-col', className)}>
      {/* Page Header */}
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container py-6 space-y-4">
          {/* Back Button */}
          {showBack && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate(-1)}
              className="gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back
            </Button>
          )}

          {/* Title and Actions */}
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-center gap-3">
              {Icon && (
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <Icon className="h-6 w-6" />
                </div>
              )}
              <div className="space-y-1">
                <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
                {displayDescription && (
                  <p className="text-muted-foreground">{displayDescription}</p>
                )}
              </div>
            </div>
            {displayActions && <div className="flex items-center gap-2">{displayActions}</div>}
          </div>
        </div>
      </div>

      {/* Page Content */}
      <div className="container py-6">{children}</div>
    </div>
  );
}
