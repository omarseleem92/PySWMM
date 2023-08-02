# Parallel Simulations and Green Infrastructure Analysis with PySWMM
PySWMM, a Python wrapper for the EPA Storm Water Management Model (SWMM), has become a powerful tool for simulating stormwater systems and analyzing their performance. Despite its capabilities, it lacks a direct approach to parallelizing simulations, which hinders the potential for executing multiple simulations in a shorter timeframe. In this article, I will show a way to run parallel simulations using PySWMM.

The SWMM model enables the representation of various combinations of green infrastructure practices (also known as Low Impact Development (LID) techniques) to investigate their effectiveness in mitigating runoff generation and enhancing water storage. The performance of the LID controls depends on several parameters. For simplicity, this article focuses only on Bio-retention cells. The Bio-retention cell consists of 4 layers: surface, soil, storage, and drain layers, as shown in Figure 1. We will vary the following parameters:
* Sub-catchment area and width.
* Ratio of Bio-retention area to the total sub-catchment area.
* Berm height of the surface layer.
* Thickness of the soil layer.
* Thickness of the storage layer.
* Seepage rate of the storage layer.

![grafik](https://github.com/omarseleem92/PySWMM/assets/57235564/ecd4e617-b9f1-43cf-aec9-d4db62d6e07b)


## SWMM model:
Adopting a similar approach to Lerer et al., 2022, in order to distinguish the rainfall-runoff process in the catchment from the hydrological processes in the LID controls, I positioned the Bio-retention cell within a sub-catchment that receives excess runoff from the upstream sub-catchment (representing the area that drains into the Bio-retention cell), as depicted in Figure 2.

![grafik](https://github.com/omarseleem92/PySWMM/assets/57235564/8bb704eb-3b4a-4bdc-a6b0-57a95d16b2d0)

## Parallelizing PySWMM simuations:
The SWMM model is not thread-safe, which means that only one model can be opened at a time per 'instance' of Python. To overcome this limitation, we can utilize a combination of queue, threading, and subprocess. This approach enables us to run each model on its own process simultaneously. The workflow is as follows:
1. Begin by listing the parameters we need to vary and store them in a Queue (a list of job descriptions).
2. Utilize threads to handle the various jobs in the queue. Each thread represents a simulation that can run in parallel, and the number of threads depends on the system's capabilities.
3. Within the worker function, call a subprocess to execute the 'pyswmm_wrapper.py' file, where we can make the desired changes to the SWMM model

## References:
Lerer, S.M., Guidje, A.H., Drenck, K.M.L., Jakobsen, C.C., Arnbjerg-Nielsen, K., Mikkelsen, P.S. and Sørup, H.J.D., 2022. Constructing an inventory for fast screening of hydraulic and hydrologic performance of stormwater control measures. Blue-Green Systems, 4(2), pp.213–229.

