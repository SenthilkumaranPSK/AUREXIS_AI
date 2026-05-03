import { describe, it, expect, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useAsync } from '../../hooks/useAsync';

describe('useAsync', () => {
  it('handles successful async operation', async () => {
    const asyncFn = vi.fn().mockResolvedValue('success');
    
    const { result } = renderHook(() => useAsync(asyncFn));
    
    expect(result.current.loading).toBe(false);
    expect(result.current.data).toBe(null);
    expect(result.current.error).toBe(null);
    
    // Execute async function
    result.current.execute();
    
    expect(result.current.loading).toBe(true);
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.data).toBe('success');
      expect(result.current.error).toBe(null);
    });
  });

  it('handles async operation failure', async () => {
    const error = new Error('Test error');
    const asyncFn = vi.fn().mockRejectedValue(error);
    
    const { result } = renderHook(() => useAsync(asyncFn));
    
    result.current.execute();
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.data).toBe(null);
      expect(result.current.error).toEqual(error);
    });
  });

  it('calls onSuccess callback', async () => {
    const onSuccess = vi.fn();
    const asyncFn = vi.fn().mockResolvedValue('success');
    
    const { result } = renderHook(() => 
      useAsync(asyncFn, { onSuccess })
    );
    
    result.current.execute();
    
    await waitFor(() => {
      expect(onSuccess).toHaveBeenCalledWith('success');
    });
  });

  it('calls onError callback', async () => {
    const onError = vi.fn();
    const error = new Error('Test error');
    const asyncFn = vi.fn().mockRejectedValue(error);
    
    const { result } = renderHook(() => 
      useAsync(asyncFn, { onError })
    );
    
    result.current.execute();
    
    await waitFor(() => {
      expect(onError).toHaveBeenCalledWith(error);
    });
  });

  it('retries on failure', async () => {
    const asyncFn = vi.fn()
      .mockRejectedValueOnce(new Error('First fail'))
      .mockRejectedValueOnce(new Error('Second fail'))
      .mockResolvedValue('success');
    
    const { result } = renderHook(() => 
      useAsync(asyncFn, { retry: 2, retryDelay: 10 })
    );
    
    result.current.execute();
    
    await waitFor(() => {
      expect(result.current.data).toBe('success');
      expect(asyncFn).toHaveBeenCalledTimes(3);
    });
  });

  it('resets state', async () => {
    const asyncFn = vi.fn().mockResolvedValue('success');
    
    const { result } = renderHook(() => useAsync(asyncFn));
    
    result.current.execute();
    
    await waitFor(() => {
      expect(result.current.data).toBe('success');
    });
    
    result.current.reset();
    
    expect(result.current.data).toBe(null);
    expect(result.current.error).toBe(null);
    expect(result.current.loading).toBe(false);
  });
});
