/**
 * Formatter Utilities Tests
 */

import { describe, it, expect } from 'vitest';
import { formatCurrency, getRiskColor, getRiskBg, getScoreColor, getScoreGradient } from '../lib/formatters';

describe('Formatters', () => {
  describe('formatCurrency', () => {
    it('should format lakhs', () => {
      expect(formatCurrency(100000)).toBe('₹1.0L');
    });

    it('should format crores', () => {
      expect(formatCurrency(10000000)).toBe('₹1.0Cr');
    });

    it('should format thousands', () => {
      expect(formatCurrency(5000)).toBe('₹5.0K');
    });

    it('should handle zero', () => {
      expect(formatCurrency(0)).toBe('₹0');
    });

    it('should format small amounts', () => {
      expect(formatCurrency(500)).toBe('₹500');
    });
  });

  describe('getRiskColor', () => {
    it('should return green for Low risk', () => {
      expect(getRiskColor('Low')).toBe('text-success');
    });

    it('should return yellow for Medium risk', () => {
      expect(getRiskColor('Medium')).toBe('text-warning');
    });

    it('should return red for High risk', () => {
      expect(getRiskColor('High')).toBe('text-danger');
    });

    it('should return red for Critical risk', () => {
      expect(getRiskColor('Critical')).toBe('text-danger');
    });

    it('should return default for unknown', () => {
      expect(getRiskColor('Unknown')).toBe('text-muted-foreground');
    });
  });

  describe('getRiskBg', () => {
    it('should return correct bg for Low risk', () => {
      expect(getRiskBg('Low')).toBe('bg-success/10 text-success border-success/20');
    });

    it('should return correct bg for Medium risk', () => {
      expect(getRiskBg('Medium')).toBe('bg-warning/10 text-warning border-warning/20');
    });

    it('should return correct bg for High risk', () => {
      expect(getRiskBg('High')).toBe('bg-danger/10 text-danger border-danger/20');
    });
  });

  describe('getScoreColor', () => {
    it('should return green for good scores', () => {
      expect(getScoreColor(85)).toBe('text-success');
    });

    it('should return yellow for average scores', () => {
      expect(getScoreColor(65)).toBe('text-warning');
    });

    it('should return red for poor scores', () => {
      expect(getScoreColor(40)).toBe('text-danger');
    });
  });

  describe('getScoreGradient', () => {
    it('should return green gradient for good scores', () => {
      expect(getScoreGradient(90)).toBe('from-success to-emerald-400');
    });

    it('should return yellow gradient for average scores', () => {
      expect(getScoreGradient(70)).toBe('from-warning to-amber-400');
    });

    it('should return red gradient for poor scores', () => {
      expect(getScoreGradient(30)).toBe('from-danger to-red-400');
    });
  });
});
