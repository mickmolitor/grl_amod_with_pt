import math
import torch
import torch.nn as nn

from params.program_params import ProgramParams

class TemporalDifferenceLoss(nn.Module):
    def __init__(self):
        super(TemporalDifferenceLoss, self).__init__()

    def forward(self, trajectories_and_state_values):
        loss = 0
        for x in trajectories_and_state_values:
            start_state_value = x[1]
            end_state_value = x[2]
            start_t = x[0]["current_time"]
            end_t = x[0]["target_time"]
            duration = end_t - start_t if end_t > start_t else 86400 - start_t + end_t
            reward = x[0]["reward"]
            loss += (
                reward
                + ProgramParams.DISCOUNT_FACTOR(duration) * end_state_value
                - start_state_value
            ) ** 2
        
        return loss