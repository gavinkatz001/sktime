from sktime.performance_metrics.detection._base import BaseDetectionMetric


class F1ScoreBreakpoints(BaseDetectionMetric):
    """F1-score for breakpoint detection, using a margin-based match criterion."""

    _tags = {
        "object_type": ["metric_detection", "metric"],
        "scitype:y": "points",  # expects each row to represent one breakpoint
        "requires_X": False,  # not using X by default
        "requires_y_true": True,  # supervised metric
        "lower_is_better": False,  # higher F1 is better
    }

    def __init__(self, margin=1.0):
        """
        Parameters
        ----------
        margin : float, optional (default=1.0)
            Margin of error to consider a breakpoint matched, i.e. |pred - true| < margin.
        """  # noqa: D205, E501
        self.margin = margin
        super().__init__()

    def _evaluate(self, y_true, y_pred, X=None):
        """Compute F1 score under the margin-based breakpoint matching logic.

        Parameters
        ----------
        y_true : pd.DataFrame
            Ground truth breakpoints in "points" format. Must have column 'ilocs'.
        y_pred : pd.DataFrame
            Predicted breakpoints in "points" format. Must have column 'ilocs'.
        X : pd.DataFrame, optional (default=None)
            Unused here, but part of the signature.

        Returns
        -------
        float
            F1 score, i.e., 2 * precision * recall / (precision + recall).
        """
        # Convert breakpoints to sorted Python lists
        # We assume the DataFrame has a column 'ilocs' with integer or float index positions  # noqa: E501
        gt = sorted(y_true["ilocs"].values)
        pred = sorted(y_pred["ilocs"].values)

        # Handle edge cases
        if len(gt) == 0 and len(pred) == 0:
            return 1.0  # No breakpoints to detect, so consider it perfect by convention
        if len(gt) == 0:
            return 0.0  # ground truth is empty but predictions exist => precision = 0 => F1=0  # noqa: E501
        if len(pred) == 0:
            return 0.0  # predictions are empty but ground truth exists => recall = 0 => F1=0  # noqa: E501

        # Count how many ground-truth breakpoints are matched
        matched_count = 0
        pred_index = 0

        for true_bkpt in gt:
            # Advance pred_index while predicted < (true - margin)
            while pred_index < len(pred) and pred[pred_index] < true_bkpt - self.margin:
                pred_index += 1

            # If current predicted is within margin, count it as matched
            if (
                pred_index < len(pred)
                and abs(pred[pred_index] - true_bkpt) < self.margin
            ):
                matched_count += 1
                # optional: pred_index += 1 to avoid double-matching the same prediction

        # Compute precision and recall
        precision = matched_count / len(pred)
        recall = matched_count / len(gt)

        # Compute F1
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)
