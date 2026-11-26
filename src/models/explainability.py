"""
ATHLETIX AI: Model Explainability & Permutation Importance Engine
================================================================
Conducts multi-angle explainability for Model A, Model B, and Model C:
- Permutation Feature Importance across cross-validation folds.
- TreeSHAP & LinearSHAP explanations.
- Multicollinearity checks via Variance Inflation Factors (VIF).
- Feature ranking stability across folds.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import shap


class ModelExplainer:
    """Manages permutation importance, SHAP values, and multicollinearity audits."""

    @staticmethod
    def compute_vif(df: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
        """
        Calculates Variance Inflation Factor (VIF) to detect multicollinearity.
        VIF > 5 indicates moderate multicollinearity; VIF > 10 indicates severe multicollinearity.
        """
        X = df[feature_cols].copy()
        imputed_X = SimpleImputer(strategy="median").fit_transform(X)
        scaled_X = StandardScaler().fit_transform(imputed_X)

        vif_data = []
        for i, col in enumerate(feature_cols):
            try:
                vif = variance_inflation_factor(scaled_X, i)
            except Exception:
                vif = np.nan
            vif_data.append({"feature": col, "vif": round(float(vif), 2) if not np.isnan(vif) else 999.0})

        vif_df = pd.DataFrame(vif_data).sort_values(by="vif", ascending=False).reset_index(drop=True)
        return vif_df

    @staticmethod
    def compute_permutation_importance(
        model_pipeline, X: np.ndarray, y: np.ndarray, feature_names: List[str], n_repeats: int = 15
    ) -> pd.DataFrame:
        """
        Computes permutation feature importance on validation sets.
        """
        result = permutation_importance(
            model_pipeline, X, y, n_repeats=n_repeats, random_state=42, scoring="neg_root_mean_squared_error"
        )
        
        importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance_mean": np.round(result.importances_mean, 4),
            "importance_std": np.round(result.importances_std, 4),
        }).sort_values(by="importance_mean", ascending=False).reset_index(drop=True)

        return importance_df

    @staticmethod
    def compute_shap_explanations(
        model_pipeline, X_df: pd.DataFrame
    ) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Calculates SHAP values for the fitted regressor.
        """
        imputer = model_pipeline.named_steps["imputer"]
        scaler = model_pipeline.named_steps["scaler"]
        regressor = model_pipeline.named_steps["regressor"]

        X_proc = scaler.transform(imputer.transform(X_df))
        
        try:
            # Tree explainer for XGBoost
            explainer = shap.TreeExplainer(regressor)
            shap_vals = explainer.shap_values(X_proc)
        except Exception:
            # Linear / Kernel explainer fallback
            explainer = shap.LinearExplainer(regressor, X_proc)
            shap_vals = explainer.shap_values(X_proc)

        mean_abs_shap = np.mean(np.abs(shap_vals), axis=0)
        shap_importance = pd.DataFrame({
            "feature": list(X_df.columns),
            "mean_abs_shap": np.round(mean_abs_shap, 4),
        }).sort_values(by="mean_abs_shap", ascending=False).reset_index(drop=True)

        return shap_vals, shap_importance
