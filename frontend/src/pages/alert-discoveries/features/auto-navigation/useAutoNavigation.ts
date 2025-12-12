import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CriticalDiscoveryDrilldown } from '../../../services/api';

interface UseAutoNavigationOptions {
  id: string | undefined;
  discoveries: CriticalDiscoveryDrilldown[];
  replace?: boolean;
}

/**
 * Hook to automatically navigate to the first discovery if no ID is provided.
 * 
 * @param id - Current discovery ID from URL params
 * @param discoveries - Array of available discoveries
 * @param replace - Whether to replace history entry (default: true)
 */
export const useAutoNavigation = ({ id, discoveries, replace = true }: UseAutoNavigationOptions) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (!id && discoveries.length > 0 && discoveries[0]?.alert_id) {
      navigate(`/alert-discoveries/${discoveries[0].alert_id}`, { replace });
    }
  }, [id, discoveries, navigate, replace]);
};

