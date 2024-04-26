import math
import torch
import torch.nn as nn

from params.program_params import ProgramParams


class TemporalDifferenceLoss(nn.Module):
    def __init__(self):
        super(TemporalDifferenceLoss, self).__init__()

    def forward(self, td_values: list[dict]):
        loss = 0
        for x in td_values:
            main_value = x["main_value"]
            target_value = x["target_value"]
            discount_value = x["discount_value"]
            reward = x["reward"]
            loss += (
                main_value
                - reward
                + discount_value * target_value
            ) ** 2

        return loss
