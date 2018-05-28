# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2016  Vesa Ojalehto
"""
Problems provided by  Narula and Weistroffer


* River pollution problem

"""
import math

from desdeo.method import NIMBUS, NAUTILUSv1
from desdeo.optimization import SciPyDE
from desdeo.preference import NIMBUSClassification
from desdeo.utils import tui

try:
    from desdeo.problem import PythonProblem, Variable
except ImportError:
    # Check if we are running from the examples
    import os
    import sys

    example_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(example_path, ".."))
    from desdeo.problem import PythonProblem, Variable


class RiverPollution(PythonProblem):
    """
    River pollution problem by Narula and Weistroffer [1]

    The problem has four objectives and two variables

    The problem describes a (hypothetical) pollution problem
    of a river, where a fishery and a city are polluting
    water. The decision variables represent the proportional
    amounts of biochemical oxygen demanding material removed
    from water in two treatment plants located after the
    fishery and after the city.

    The first and second objective functions describe the
    quality of water after the fishery and after the city,
    respectively, while objective functions three and four
    represent the percent return on investment at the fishery
    and the addition to the tax rate in the
    city. respectively.


    References
    ----------

    [1] Narula, S. & Weistroffer, H. A flexible method for
      nonlinear multicriteria decision-making problems
      Systems, IEEE Transactions on Man and Cybernetics,
      1989, 19, 883-887.
"""

    def __init__(self):
        super().__init__(
            nobj=4,
            nconst=0,  # Optional
            ideal=[-6.34, -3.44, -7.5, 0.1],  # Optional
            nadir=[-4.07, -2.87, -0.32, 9.71],  # Optional
            maximized=[True, True, True, False],  # Optional
            objectives=[
                "Water Quality Fishery",  # Optional
                "Water Quality City",
                "Fishery ROI",
                "City Tax Increase",
            ],
            name="River pollution method",  # Optional
        )
        self.add_variables(
            Variable([0.0, 1.0], starting_point=0.5, name="BOD City")  # Optional
        )  # Optional
        self.add_variables(
            Variable([0.0, 1.0], starting_point=0.5, name="BOD City")  # Optional
        )  # Optional

    def evaluate(self, population):
        objectives = []

        for values in population:
            res = []
            x0_2 = math.pow(values[0], 2)
            x1_2 = math.pow(values[1], 2)

            res.append(-1.0 * (4.07 + 2.27 * values[0]))

            res.append(
                -1.0
                * (
                    2.6
                    + 0.03 * values[0]
                    + 0.02 * values[1]
                    + 0.01 / (1.39 - x1_2)
                    + 0.3 / (1.39 - x1_2)
                )
            )

            res.append(-1.0 * (8.21 - 0.71 / (1.09 - x0_2)))

            res.append(-1.0 * (0.96 - 0.96 / (1.09 - x1_2)))

            objectives.append(res)

        return objectives


if __name__ == "__main__":
    # Solve River Pollution problem using NAUTILUS
    # Using tui
    print("Solve with NAUTILUS method")
    natmeth = NAUTILUSv1(RiverPollution(), SciPyDE)
    NAUTILUS_solution = tui.iter_nautilus(natmeth)
    print("NAUTILUS solution")
    print(NAUTILUS_solution)
    # Output:
    # [-6.2927077117830965, -3.4038593790999485,
    #   -7.401394350956817, 1.6201876469013787]

    # Continue solving  River Pollution problem
    # From NAUTILUS solution

    nimmeth = NIMBUS(RiverPollution(), SciPyDE)
    nimmeth.init_iteration()
    print("Solving with NIMBUS method")
    class1 = NIMBUSClassification(
        nimmeth, [(">=", -5.5), (">=", -3.0), ("<=", -6.5), ("<=", -2.0)]
    )
    iter1 = nimmeth.next_iteration(preference=class1)
    print("NIMBUS solutions")
    print(iter1)
    # Output
    # [[-5.685179670183404, -2.845500670078188, -6.9936653595242255, -0.07781863514782916],
    #  [-6.104997526730949, -2.8792454934814242, -5.730370900831871, 0.03584500974406313]]
