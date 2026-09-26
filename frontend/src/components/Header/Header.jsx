import React from 'react';
import StatusBadge from '../StatusBadge';

export default function Header({ analysisData }) {
  if (!analysisData) return null;

  return (
    <div style={{
      background: 'var(--color-surface)',
      border: '1px solid var(--color-border)',
      borderRadius: 'var(--radius-md)',
      padding: '14px 24px',
      marginBottom: '24px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      boxShadow: 'var(--shadow-sm)'
    }}>
      <div>
        <div style={{ fontSize: '11px', fontWeight: '700', color: 'var(--color-brand)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
          Audited Model
        </div>
        <div style={{ fontSize: '16px', fontWeight: '800', color: 'var(--color-text-primary)' }}>
          {analysisData.model_name}
        </div>
      </div>

      <div style={{ display: 'flex', gap: '30px', alignItems: 'center' }}>
        <div>
          <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', fontWeight: '600', textTransform: 'uppercase' }}>
            Risk Tier
          </div>
          <div style={{ fontSize: '13px', fontWeight: '700', color: 'var(--color-text-secondary)', textTransform: 'capitalize' }}>
            {analysisData.risk_tier}
          </div>
        </div>

        <div>
          <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', fontWeight: '600', textTransform: 'uppercase' }}>
            Total Samples
          </div>
          <div style={{ fontSize: '13px', fontWeight: '700', color: 'var(--color-text-secondary)' }}>
            {analysisData.total_samples.toLocaleString()}
          </div>
        </div>

        <div>
          <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', fontWeight: '600', textTransform: 'uppercase' }}>
            Fairness Score
          </div>
          <div style={{ fontSize: '15px', fontWeight: '800', color: 'var(--color-brand)' }}>
            {analysisData.overall_fairness_score}%
          </div>
        </div>

        <div>
          <StatusBadge status={analysisData.overall_status} />
        </div>
      </div>
    </div>
  );
}
