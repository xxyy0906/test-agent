# 1202 全部对象默认值清单（按 OID）


| 项      | 值                                            |
| ------ | -------------------------------------------- |
| MIB    | `mibs/mibs_old/1202v0218.mib`                |
| 对象数    | **253**                                      |
| OID 范围 | `1.3.6.1.4.1.1206.4.2.1` (asc)               |
| 表实例    | `dev_cap=1`（每列展示第 1 行实例 OID 与值）              |
| 规则     | 见 [1202DEFAULT_DATA.md](1202DEFAULT_DATA.md) |


## 清单


| #   | 对象名                                | 类型     | 定义 OID                             | 实例 OID (row 1)                       | ACCESS         | 默认值                                                          |
| --- | ---------------------------------- | ------ | ---------------------------------- | ------------------------------------ | -------------- | ------------------------------------------------------------ |
| 1   | `phase`                            | branch | `1.3.6.1.4.1.1206.4.2.1.1`         | `—`                                  | read-only      | —                                                            |
| 2   | `maxPhases`                        | scalar | `1.3.6.1.4.1.1206.4.2.1.1.1`       | `1.3.6.1.4.1.1206.4.2.1.1.1.0`       | read-only      | 255                                                          |
| 3   | `phaseTable`                       | table  | `1.3.6.1.4.1.1206.4.2.1.1.2`       | `—`                                  | not-accessible | —                                                            |
| 4   | `phaseEntry`                       | entry  | `1.3.6.1.4.1.1206.4.2.1.1.2.1`     | `—`                                  | not-accessible | —                                                            |
| 5   | `phaseNumber`                      | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.1`   | `1.3.6.1.4.1.1206.4.2.1.1.2.1.1.1`   | read-only      | 1                                                            |
| 6   | `phaseRedRevert`                   | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.10`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.10.1`  | read-write     | 255                                                          |
| 7   | `phaseAddedInitial`                | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.11`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.11.1`  | read-write     | 255                                                          |
| 8   | `phaseMaximumInitial`              | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.12`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.12.1`  | read-write     | 255                                                          |
| 9   | `phaseTimeBeforeReduction`         | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.13`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.13.1`  | read-write     | 255                                                          |
| 10  | `phaseCarsBeforeReduction`         | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.14`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.14.1`  | read-write     | 255                                                          |
| 11  | `phaseTimeToReduce`                | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.15`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.15.1`  | read-write     | 255                                                          |
| 12  | `phaseReduceBy`                    | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.16`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.16.1`  | read-write     | 255                                                          |
| 13  | `phaseMinimumGap`                  | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.17`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.17.1`  | read-write     | 255                                                          |
| 14  | `phaseDynamicMaxLimit`             | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.18`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.18.1`  | read-write     | 255                                                          |
| 15  | `phaseDynamicMaxStep`              | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.19`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.19.1`  | read-write     | 255                                                          |
| 16  | `phaseWalk`                        | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.2`   | `1.3.6.1.4.1.1206.4.2.1.1.2.1.2.1`   | read-write     | 255                                                          |
| 17  | `phaseStartup`                     | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.20`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.20.1`  | read-write     | 6                                                            |
| 18  | `phaseOptions`                     | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.21`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.21.1`  | read-write     | 65535                                                        |
| 19  | `phaseRing`                        | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.22`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.22.1`  | read-write     | 255                                                          |
| 20  | `phaseConcurrency`                 | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.23`  | `1.3.6.1.4.1.1206.4.2.1.1.2.1.23.1`  | read-write     | 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ... (255 bytes) |
| 21  | `phasePedestrianClear`             | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.3`   | `1.3.6.1.4.1.1206.4.2.1.1.2.1.3.1`   | read-write     | 255                                                          |
| 22  | `phaseMinimumGreen`                | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.4`   | `1.3.6.1.4.1.1206.4.2.1.1.2.1.4.1`   | read-write     | 255                                                          |
| 23  | `phasePassage`                     | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.5`   | `1.3.6.1.4.1.1206.4.2.1.1.2.1.5.1`   | read-write     | 255                                                          |
| 24  | `phaseMaximum1`                    | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.6`   | `1.3.6.1.4.1.1206.4.2.1.1.2.1.6.1`   | read-write     | 255                                                          |
| 25  | `phaseMaximum2`                    | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.7`   | `1.3.6.1.4.1.1206.4.2.1.1.2.1.7.1`   | read-write     | 255                                                          |
| 26  | `phaseYellowChange`                | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.8`   | `1.3.6.1.4.1.1206.4.2.1.1.2.1.8.1`   | read-write     | 255                                                          |
| 27  | `phaseRedClear`                    | column | `1.3.6.1.4.1.1206.4.2.1.1.2.1.9`   | `1.3.6.1.4.1.1206.4.2.1.1.2.1.9.1`   | read-write     | 255                                                          |
| 28  | `maxPhaseGroups`                   | scalar | `1.3.6.1.4.1.1206.4.2.1.1.3`       | `1.3.6.1.4.1.1206.4.2.1.1.3.0`       | read-only      | 255                                                          |
| 29  | `phaseStatusGroupTable`            | table  | `1.3.6.1.4.1.1206.4.2.1.1.4`       | `—`                                  | not-accessible | —                                                            |
| 30  | `phaseStatusGroupEntry`            | entry  | `1.3.6.1.4.1.1206.4.2.1.1.4.1`     | `—`                                  | not-accessible | —                                                            |
| 31  | `phaseStatusGroupNumber`           | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.1`   | `1.3.6.1.4.1.1206.4.2.1.1.4.1.1.1`   | read-only      | 1                                                            |
| 32  | `phaseStatusGroupPhaseOns`         | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.10`  | `1.3.6.1.4.1.1206.4.2.1.1.4.1.10.1`  | read-only      | 255                                                          |
| 33  | `phaseStatusGroupPhaseNexts`       | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.11`  | `1.3.6.1.4.1.1206.4.2.1.1.4.1.11.1`  | read-only      | 255                                                          |
| 34  | `phaseStatusGroupReds`             | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.2`   | `1.3.6.1.4.1.1206.4.2.1.1.4.1.2.1`   | read-only      | 255                                                          |
| 35  | `phaseStatusGroupYellows`          | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.3`   | `1.3.6.1.4.1.1206.4.2.1.1.4.1.3.1`   | read-only      | 255                                                          |
| 36  | `phaseStatusGroupGreens`           | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.4`   | `1.3.6.1.4.1.1206.4.2.1.1.4.1.4.1`   | read-only      | 255                                                          |
| 37  | `phaseStatusGroupDontWalks`        | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.5`   | `1.3.6.1.4.1.1206.4.2.1.1.4.1.5.1`   | read-only      | 255                                                          |
| 38  | `phaseStatusGroupPedClears`        | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.6`   | `1.3.6.1.4.1.1206.4.2.1.1.4.1.6.1`   | read-only      | 255                                                          |
| 39  | `phaseStatusGroupWalks`            | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.7`   | `1.3.6.1.4.1.1206.4.2.1.1.4.1.7.1`   | read-only      | 255                                                          |
| 40  | `phaseStatusGroupVehCalls`         | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.8`   | `1.3.6.1.4.1.1206.4.2.1.1.4.1.8.1`   | read-only      | 255                                                          |
| 41  | `phaseStatusGroupPedCalls`         | column | `1.3.6.1.4.1.1206.4.2.1.1.4.1.9`   | `1.3.6.1.4.1.1206.4.2.1.1.4.1.9.1`   | read-only      | 255                                                          |
| 42  | `phaseControlGroupTable`           | table  | `1.3.6.1.4.1.1206.4.2.1.1.5`       | `—`                                  | not-accessible | —                                                            |
| 43  | `phaseControlGroupEntry`           | entry  | `1.3.6.1.4.1.1206.4.2.1.1.5.1`     | `—`                                  | not-accessible | —                                                            |
| 44  | `phaseControlGroupNumber`          | column | `1.3.6.1.4.1.1206.4.2.1.1.5.1.1`   | `1.3.6.1.4.1.1206.4.2.1.1.5.1.1.1`   | read-only      | 1                                                            |
| 45  | `phaseControlGroupPhaseOmit`       | column | `1.3.6.1.4.1.1206.4.2.1.1.5.1.2`   | `1.3.6.1.4.1.1206.4.2.1.1.5.1.2.1`   | read-write     | 255                                                          |
| 46  | `phaseControlGroupPedOmit`         | column | `1.3.6.1.4.1.1206.4.2.1.1.5.1.3`   | `1.3.6.1.4.1.1206.4.2.1.1.5.1.3.1`   | read-write     | 255                                                          |
| 47  | `phaseControlGroupHold`            | column | `1.3.6.1.4.1.1206.4.2.1.1.5.1.4`   | `1.3.6.1.4.1.1206.4.2.1.1.5.1.4.1`   | read-write     | 255                                                          |
| 48  | `phaseControlGroupForceOff`        | column | `1.3.6.1.4.1.1206.4.2.1.1.5.1.5`   | `1.3.6.1.4.1.1206.4.2.1.1.5.1.5.1`   | read-write     | 255                                                          |
| 49  | `phaseControlGroupVehCall`         | column | `1.3.6.1.4.1.1206.4.2.1.1.5.1.6`   | `1.3.6.1.4.1.1206.4.2.1.1.5.1.6.1`   | read-write     | 255                                                          |
| 50  | `phaseControlGroupPedCall`         | column | `1.3.6.1.4.1.1206.4.2.1.1.5.1.7`   | `1.3.6.1.4.1.1206.4.2.1.1.5.1.7.1`   | read-write     | 255                                                          |
| 51  | `ts2port1`                         | branch | `1.3.6.1.4.1.1206.4.2.1.10`        | `—`                                  | read-only      | —                                                            |
| 52  | `maxPort1Addresses`                | scalar | `1.3.6.1.4.1.1206.4.2.1.10.1`      | `1.3.6.1.4.1.1206.4.2.1.10.1.0`      | read-only      | 255                                                          |
| 53  | `port1Table`                       | table  | `1.3.6.1.4.1.1206.4.2.1.10.2`      | `—`                                  | not-accessible | —                                                            |
| 54  | `port1Entry`                       | entry  | `1.3.6.1.4.1.1206.4.2.1.10.2.1`    | `—`                                  | not-accessible | —                                                            |
| 55  | `port1Number`                      | column | `1.3.6.1.4.1.1206.4.2.1.10.2.1.1`  | `1.3.6.1.4.1.1206.4.2.1.10.2.1.1.1`  | read-only      | 1                                                            |
| 56  | `port1DevicePresent`               | column | `1.3.6.1.4.1.1206.4.2.1.10.2.1.2`  | `1.3.6.1.4.1.1206.4.2.1.10.2.1.2.1`  | read-write     | 1                                                            |
| 57  | `port1Frame40Enable`               | column | `1.3.6.1.4.1.1206.4.2.1.10.2.1.3`  | `1.3.6.1.4.1.1206.4.2.1.10.2.1.3.1`  | read-write     | 1                                                            |
| 58  | `port1Status`                      | column | `1.3.6.1.4.1.1206.4.2.1.10.2.1.4`  | `1.3.6.1.4.1.1206.4.2.1.10.2.1.4.1`  | read-only      | 3                                                            |
| 59  | `port1FaultFrame`                  | column | `1.3.6.1.4.1.1206.4.2.1.10.2.1.5`  | `1.3.6.1.4.1.1206.4.2.1.10.2.1.5.1`  | read-only      | 255                                                          |
| 60  | `ascBlock`                         | branch | `1.3.6.1.4.1.1206.4.2.1.11`        | `—`                                  | read-only      | —                                                            |
| 61  | `ascBlockGetControl`               | scalar | `1.3.6.1.4.1.1206.4.2.1.11.1`      | `1.3.6.1.4.1.1206.4.2.1.11.1.0`      | read-write     | 'ZZZZZZZZZZZZ'                                               |
| 62  | `ascBlockData`                     | scalar | `1.3.6.1.4.1.1206.4.2.1.11.2`      | `1.3.6.1.4.1.1206.4.2.1.11.2.0`      | read-write     | 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ... (255 bytes) |
| 63  | `ascBlockErrorStatus`              | scalar | `1.3.6.1.4.1.1206.4.2.1.11.3`      | `1.3.6.1.4.1.1206.4.2.1.11.3.0`      | read-only      | 65535                                                        |
| 64  | `detector`                         | branch | `1.3.6.1.4.1.1206.4.2.1.2`         | `—`                                  | read-only      | —                                                            |
| 65  | `maxVehicleDetectors`              | scalar | `1.3.6.1.4.1.1206.4.2.1.2.1`       | `1.3.6.1.4.1.1206.4.2.1.2.1.0`       | read-only      | 255                                                          |
| 66  | `vehicleDetectorTable`             | table  | `1.3.6.1.4.1.1206.4.2.1.2.2`       | `—`                                  | not-accessible | —                                                            |
| 67  | `vehicleDetectorEntry`             | entry  | `1.3.6.1.4.1.1206.4.2.1.2.2.1`     | `—`                                  | not-accessible | —                                                            |
| 68  | `vehicleDetectorNumber`            | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.1`   | `1.3.6.1.4.1.1206.4.2.1.2.2.1.1.1`   | read-only      | 1                                                            |
| 69  | `vehicleDetectorMaxPresence`       | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.10`  | `1.3.6.1.4.1.1206.4.2.1.2.2.1.10.1`  | read-write     | 255                                                          |
| 70  | `vehicleDetectorErraticCounts`     | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.11`  | `1.3.6.1.4.1.1206.4.2.1.2.2.1.11.1`  | read-write     | 255                                                          |
| 71  | `vehicleDetectorFailTime`          | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.12`  | `1.3.6.1.4.1.1206.4.2.1.2.2.1.12.1`  | read-write     | 255                                                          |
| 72  | `vehicleDetectorAlarms`            | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.13`  | `1.3.6.1.4.1.1206.4.2.1.2.2.1.13.1`  | read-only      | 255                                                          |
| 73  | `vehicleDetectorReportedAlarms`    | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.14`  | `1.3.6.1.4.1.1206.4.2.1.2.2.1.14.1`  | read-only      | 255                                                          |
| 74  | `vehicleDetectorReset`             | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.15`  | `1.3.6.1.4.1.1206.4.2.1.2.2.1.15.1`  | read-write     | 1                                                            |
| 75  | `vehicleDetectorOptions`           | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.2`   | `1.3.6.1.4.1.1206.4.2.1.2.2.1.2.1`   | read-write     | 255                                                          |
| 76  | `vehicleDetectorCallPhase`         | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.4`   | `1.3.6.1.4.1.1206.4.2.1.2.2.1.4.1`   | read-write     | 255                                                          |
| 77  | `vehicleDetectorSwitchPhase`       | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.5`   | `1.3.6.1.4.1.1206.4.2.1.2.2.1.5.1`   | read-write     | 255                                                          |
| 78  | `vehicleDetectorDelay`             | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.6`   | `1.3.6.1.4.1.1206.4.2.1.2.2.1.6.1`   | read-write     | 65535                                                        |
| 79  | `vehicleDetectorExtend`            | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.7`   | `1.3.6.1.4.1.1206.4.2.1.2.2.1.7.1`   | read-write     | 255                                                          |
| 80  | `vehicleDetectorQueueLimit`        | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.8`   | `1.3.6.1.4.1.1206.4.2.1.2.2.1.8.1`   | read-write     | 255                                                          |
| 81  | `vehicleDetectorNoActivity`        | column | `1.3.6.1.4.1.1206.4.2.1.2.2.1.9`   | `1.3.6.1.4.1.1206.4.2.1.2.2.1.9.1`   | read-write     | 255                                                          |
| 82  | `maxVehicleDetectorStatusGroups`   | scalar | `1.3.6.1.4.1.1206.4.2.1.2.3`       | `1.3.6.1.4.1.1206.4.2.1.2.3.0`       | read-only      | 255                                                          |
| 83  | `vehicleDetectorStatusGroupTable`  | table  | `1.3.6.1.4.1.1206.4.2.1.2.4`       | `—`                                  | not-accessible | —                                                            |
| 84  | `vehicleDetectorStatusGroupEntry`  | entry  | `1.3.6.1.4.1.1206.4.2.1.2.4.1`     | `—`                                  | not-accessible | —                                                            |
| 85  | `vehicleDetectorStatusGroupNumber` | column | `1.3.6.1.4.1.1206.4.2.1.2.4.1.1`   | `1.3.6.1.4.1.1206.4.2.1.2.4.1.1.1`   | read-only      | 1                                                            |
| 86  | `vehicleDetectorStatusGroupActive` | column | `1.3.6.1.4.1.1206.4.2.1.2.4.1.2`   | `1.3.6.1.4.1.1206.4.2.1.2.4.1.2.1`   | read-only      | 255                                                          |
| 87  | `vehicleDetectorStatusGroupAlarms` | column | `1.3.6.1.4.1.1206.4.2.1.2.4.1.3`   | `1.3.6.1.4.1.1206.4.2.1.2.4.1.3.1`   | read-only      | 255                                                          |
| 88  | `volumeOccupancyReport`            | branch | `1.3.6.1.4.1.1206.4.2.1.2.5`       | `—`                                  | read-only      | —                                                            |
| 89  | `volumeOccupancySequence`          | scalar | `1.3.6.1.4.1.1206.4.2.1.2.5.1`     | `1.3.6.1.4.1.1206.4.2.1.2.5.1.0`     | read-only      | 255                                                          |
| 90  | `volumeOccupancyPeriod`            | scalar | `1.3.6.1.4.1.1206.4.2.1.2.5.2`     | `1.3.6.1.4.1.1206.4.2.1.2.5.2.0`     | read-write     | 255                                                          |
| 91  | `activeVolumeOccupancyDetectors`   | scalar | `1.3.6.1.4.1.1206.4.2.1.2.5.3`     | `1.3.6.1.4.1.1206.4.2.1.2.5.3.0`     | read-only      | 255                                                          |
| 92  | `volumeOccupancyTable`             | table  | `1.3.6.1.4.1.1206.4.2.1.2.5.4`     | `—`                                  | not-accessible | —                                                            |
| 93  | `volumeOccupancyEntry`             | entry  | `1.3.6.1.4.1.1206.4.2.1.2.5.4.1`   | `—`                                  | not-accessible | —                                                            |
| 94  | `detectorVolume`                   | column | `1.3.6.1.4.1.1206.4.2.1.2.5.4.1.1` | `1.3.6.1.4.1.1206.4.2.1.2.5.4.1.1.1` | read-only      | 255                                                          |
| 95  | `detectorOccupancy`                | column | `1.3.6.1.4.1.1206.4.2.1.2.5.4.1.2` | `1.3.6.1.4.1.1206.4.2.1.2.5.4.1.2.1` | read-only      | 255                                                          |
| 96  | `maxPedestrianDetectors`           | scalar | `1.3.6.1.4.1.1206.4.2.1.2.6`       | `1.3.6.1.4.1.1206.4.2.1.2.6.0`       | read-only      | 255                                                          |
| 97  | `pedestrianDetectorTable`          | table  | `1.3.6.1.4.1.1206.4.2.1.2.7`       | `—`                                  | not-accessible | —                                                            |
| 98  | `pedestrianDetectorEntry`          | entry  | `1.3.6.1.4.1.1206.4.2.1.2.7.1`     | `—`                                  | not-accessible | —                                                            |
| 99  | `pedestrianDetectorNumber`         | column | `1.3.6.1.4.1.1206.4.2.1.2.7.1.1`   | `1.3.6.1.4.1.1206.4.2.1.2.7.1.1.1`   | read-only      | 1                                                            |
| 100 | `pedestrianDetectorCallPhase`      | column | `1.3.6.1.4.1.1206.4.2.1.2.7.1.2`   | `1.3.6.1.4.1.1206.4.2.1.2.7.1.2.1`   | read-write     | 255                                                          |
| 101 | `pedestrianDetectorNoActivity`     | column | `1.3.6.1.4.1.1206.4.2.1.2.7.1.3`   | `1.3.6.1.4.1.1206.4.2.1.2.7.1.3.1`   | read-write     | 255                                                          |
| 102 | `pedestrianDetectorMaxPresence`    | column | `1.3.6.1.4.1.1206.4.2.1.2.7.1.4`   | `1.3.6.1.4.1.1206.4.2.1.2.7.1.4.1`   | read-write     | 255                                                          |
| 103 | `pedestrianDetectorErraticCounts`  | column | `1.3.6.1.4.1.1206.4.2.1.2.7.1.5`   | `1.3.6.1.4.1.1206.4.2.1.2.7.1.5.1`   | read-write     | 255                                                          |
| 104 | `pedestrianDetectorAlarms`         | column | `1.3.6.1.4.1.1206.4.2.1.2.7.1.6`   | `1.3.6.1.4.1.1206.4.2.1.2.7.1.6.1`   | read-only      | 255                                                          |
| 105 | `unit`                             | branch | `1.3.6.1.4.1.1206.4.2.1.3`         | `—`                                  | read-only      | —                                                            |
| 106 | `unitStartUpFlash`                 | scalar | `1.3.6.1.4.1.1206.4.2.1.3.1`       | `1.3.6.1.4.1.1206.4.2.1.3.1.0`       | read-write     | 255                                                          |
| 107 | `unitControl`                      | scalar | `1.3.6.1.4.1.1206.4.2.1.3.10`      | `1.3.6.1.4.1.1206.4.2.1.3.10.0`      | read-write     | 255                                                          |
| 108 | `maxAlarmGroups`                   | scalar | `1.3.6.1.4.1.1206.4.2.1.3.11`      | `1.3.6.1.4.1.1206.4.2.1.3.11.0`      | read-only      | 255                                                          |
| 109 | `alarmGroupTable`                  | table  | `1.3.6.1.4.1.1206.4.2.1.3.12`      | `—`                                  | not-accessible | —                                                            |
| 110 | `alarmGroupEntry`                  | entry  | `1.3.6.1.4.1.1206.4.2.1.3.12.1`    | `—`                                  | not-accessible | —                                                            |
| 111 | `alarmGroupNumber`                 | column | `1.3.6.1.4.1.1206.4.2.1.3.12.1.1`  | `1.3.6.1.4.1.1206.4.2.1.3.12.1.1.1`  | read-only      | 1                                                            |
| 112 | `alarmGroupState`                  | column | `1.3.6.1.4.1.1206.4.2.1.3.12.1.2`  | `1.3.6.1.4.1.1206.4.2.1.3.12.1.2.1`  | read-only      | 255                                                          |
| 113 | `maxSpecialFunctionOutputs`        | scalar | `1.3.6.1.4.1.1206.4.2.1.3.13`      | `1.3.6.1.4.1.1206.4.2.1.3.13.0`      | read-only      | 255                                                          |
| 114 | `specialFunctionOutputTable`       | table  | `1.3.6.1.4.1.1206.4.2.1.3.14`      | `—`                                  | not-accessible | —                                                            |
| 115 | `specialFunctionOutputEntry`       | entry  | `1.3.6.1.4.1.1206.4.2.1.3.14.1`    | `—`                                  | not-accessible | —                                                            |
| 116 | `specialFunctionOutputNumber`      | column | `1.3.6.1.4.1.1206.4.2.1.3.14.1.1`  | `1.3.6.1.4.1.1206.4.2.1.3.14.1.1.1`  | read-only      | 1                                                            |
| 117 | `specialFunctionOutputControl`     | column | `1.3.6.1.4.1.1206.4.2.1.3.14.1.3`  | `1.3.6.1.4.1.1206.4.2.1.3.14.1.3.1`  | read-write     | 1                                                            |
| 118 | `specialFunctionOutputStatus`      | column | `1.3.6.1.4.1.1206.4.2.1.3.14.1.4`  | `1.3.6.1.4.1.1206.4.2.1.3.14.1.4.1`  | read-only      | 1                                                            |
| 119 | `unitAutoPedestrianClear`          | scalar | `1.3.6.1.4.1.1206.4.2.1.3.2`       | `1.3.6.1.4.1.1206.4.2.1.3.2.0`       | read-write     | 2                                                            |
| 120 | `unitBackupTime`                   | scalar | `1.3.6.1.4.1.1206.4.2.1.3.3`       | `1.3.6.1.4.1.1206.4.2.1.3.3.0`       | read-write     | 65535                                                        |
| 121 | `unitRedRevert`                    | scalar | `1.3.6.1.4.1.1206.4.2.1.3.4`       | `1.3.6.1.4.1.1206.4.2.1.3.4.0`       | read-write     | 255                                                          |
| 122 | `unitControlStatus`                | scalar | `1.3.6.1.4.1.1206.4.2.1.3.5`       | `1.3.6.1.4.1.1206.4.2.1.3.5.0`       | read-only      | 8                                                            |
| 123 | `unitFlashStatus`                  | scalar | `1.3.6.1.4.1.1206.4.2.1.3.6`       | `1.3.6.1.4.1.1206.4.2.1.3.6.0`       | read-only      | 8                                                            |
| 124 | `unitAlarmStatus2`                 | scalar | `1.3.6.1.4.1.1206.4.2.1.3.7`       | `1.3.6.1.4.1.1206.4.2.1.3.7.0`       | read-only      | 255                                                          |
| 125 | `unitAlarmStatus1`                 | scalar | `1.3.6.1.4.1.1206.4.2.1.3.8`       | `1.3.6.1.4.1.1206.4.2.1.3.8.0`       | read-only      | 255                                                          |
| 126 | `shortAlarmStatus`                 | scalar | `1.3.6.1.4.1.1206.4.2.1.3.9`       | `1.3.6.1.4.1.1206.4.2.1.3.9.0`       | read-only      | 255                                                          |
| 127 | `coord`                            | branch | `1.3.6.1.4.1.1206.4.2.1.4`         | `—`                                  | read-only      | —                                                            |
| 128 | `coordOperationalMode`             | scalar | `1.3.6.1.4.1.1206.4.2.1.4.1`       | `1.3.6.1.4.1.1206.4.2.1.4.1.0`       | read-write     | 255                                                          |
| 129 | `coordPatternStatus`               | scalar | `1.3.6.1.4.1.1206.4.2.1.4.10`      | `1.3.6.1.4.1.1206.4.2.1.4.10.0`      | read-only      | 255                                                          |
| 130 | `localFreeStatus`                  | scalar | `1.3.6.1.4.1.1206.4.2.1.4.11`      | `1.3.6.1.4.1.1206.4.2.1.4.11.0`      | read-only      | 11                                                           |
| 131 | `coordCycleStatus`                 | scalar | `1.3.6.1.4.1.1206.4.2.1.4.12`      | `1.3.6.1.4.1.1206.4.2.1.4.12.0`      | read-only      | 510                                                          |
| 132 | `coordSyncStatus`                  | scalar | `1.3.6.1.4.1.1206.4.2.1.4.13`      | `1.3.6.1.4.1.1206.4.2.1.4.13.0`      | read-only      | 510                                                          |
| 133 | `systemPatternControl`             | scalar | `1.3.6.1.4.1.1206.4.2.1.4.14`      | `1.3.6.1.4.1.1206.4.2.1.4.14.0`      | read-write     | 255                                                          |
| 134 | `systemSyncControl`                | scalar | `1.3.6.1.4.1.1206.4.2.1.4.15`      | `1.3.6.1.4.1.1206.4.2.1.4.15.0`      | read-write     | 255                                                          |
| 135 | `coordCorrectionMode`              | scalar | `1.3.6.1.4.1.1206.4.2.1.4.2`       | `1.3.6.1.4.1.1206.4.2.1.4.2.0`       | read-write     | 4                                                            |
| 136 | `coordMaximumMode`                 | scalar | `1.3.6.1.4.1.1206.4.2.1.4.3`       | `1.3.6.1.4.1.1206.4.2.1.4.3.0`       | read-write     | 4                                                            |
| 137 | `coordForceMode`                   | scalar | `1.3.6.1.4.1.1206.4.2.1.4.4`       | `1.3.6.1.4.1.1206.4.2.1.4.4.0`       | read-write     | 3                                                            |
| 138 | `maxPatterns`                      | scalar | `1.3.6.1.4.1.1206.4.2.1.4.5`       | `1.3.6.1.4.1.1206.4.2.1.4.5.0`       | read-only      | 253                                                          |
| 139 | `patternTableType`                 | scalar | `1.3.6.1.4.1.1206.4.2.1.4.6`       | `1.3.6.1.4.1.1206.4.2.1.4.6.0`       | read-only      | 4                                                            |
| 140 | `patternTable`                     | table  | `1.3.6.1.4.1.1206.4.2.1.4.7`       | `—`                                  | not-accessible | —                                                            |
| 141 | `patternEntry`                     | entry  | `1.3.6.1.4.1.1206.4.2.1.4.7.1`     | `—`                                  | not-accessible | —                                                            |
| 142 | `patternNumber`                    | column | `1.3.6.1.4.1.1206.4.2.1.4.7.1.1`   | `1.3.6.1.4.1.1206.4.2.1.4.7.1.1.1`   | read-only      | 1                                                            |
| 143 | `patternCycleTime`                 | column | `1.3.6.1.4.1.1206.4.2.1.4.7.1.2`   | `1.3.6.1.4.1.1206.4.2.1.4.7.1.2.1`   | read-write     | 255                                                          |
| 144 | `patternOffsetTime`                | column | `1.3.6.1.4.1.1206.4.2.1.4.7.1.3`   | `1.3.6.1.4.1.1206.4.2.1.4.7.1.3.1`   | read-write     | 255                                                          |
| 145 | `patternSplitNumber`               | column | `1.3.6.1.4.1.1206.4.2.1.4.7.1.4`   | `1.3.6.1.4.1.1206.4.2.1.4.7.1.4.1`   | read-only      | 255                                                          |
| 146 | `patternSequenceNumber`            | column | `1.3.6.1.4.1.1206.4.2.1.4.7.1.5`   | `1.3.6.1.4.1.1206.4.2.1.4.7.1.5.1`   | read-write     | 255                                                          |
| 147 | `maxSplits`                        | scalar | `1.3.6.1.4.1.1206.4.2.1.4.8`       | `1.3.6.1.4.1.1206.4.2.1.4.8.0`       | read-only      | 255                                                          |
| 148 | `splitTable`                       | table  | `1.3.6.1.4.1.1206.4.2.1.4.9`       | `—`                                  | not-accessible | —                                                            |
| 149 | `splitEntry`                       | entry  | `1.3.6.1.4.1.1206.4.2.1.4.9.1`     | `—`                                  | not-accessible | —                                                            |
| 150 | `splitNumber`                      | column | `1.3.6.1.4.1.1206.4.2.1.4.9.1.1`   | `1.3.6.1.4.1.1206.4.2.1.4.9.1.1.1.1` | read-only      | 1                                                            |
| 151 | `splitPhase`                       | column | `1.3.6.1.4.1.1206.4.2.1.4.9.1.2`   | `1.3.6.1.4.1.1206.4.2.1.4.9.1.2.1.1` | read-only      | 1                                                            |
| 152 | `splitTime`                        | column | `1.3.6.1.4.1.1206.4.2.1.4.9.1.3`   | `1.3.6.1.4.1.1206.4.2.1.4.9.1.3.1.1` | read-write     | 255                                                          |
| 153 | `splitMode`                        | column | `1.3.6.1.4.1.1206.4.2.1.4.9.1.4`   | `1.3.6.1.4.1.1206.4.2.1.4.9.1.4.1.1` | read-write     | 7                                                            |
| 154 | `splitCoordPhase`                  | column | `1.3.6.1.4.1.1206.4.2.1.4.9.1.5`   | `1.3.6.1.4.1.1206.4.2.1.4.9.1.5.1.1` | read-write     | 1                                                            |
| 155 | `timebaseAsc`                      | branch | `1.3.6.1.4.1.1206.4.2.1.5`         | `—`                                  | read-only      | —                                                            |
| 156 | `timebaseAscPatternSync`           | scalar | `1.3.6.1.4.1.1206.4.2.1.5.1`       | `1.3.6.1.4.1.1206.4.2.1.5.1.0`       | read-write     | 65535                                                        |
| 157 | `maxTimebaseAscActions`            | scalar | `1.3.6.1.4.1.1206.4.2.1.5.2`       | `1.3.6.1.4.1.1206.4.2.1.5.2.0`       | read-only      | 255                                                          |
| 158 | `timebaseAscActionTable`           | table  | `1.3.6.1.4.1.1206.4.2.1.5.3`       | `—`                                  | not-accessible | —                                                            |
| 159 | `timebaseAscActionEntry`           | entry  | `1.3.6.1.4.1.1206.4.2.1.5.3.1`     | `—`                                  | not-accessible | —                                                            |
| 160 | `timebaseAscActionNumber`          | column | `1.3.6.1.4.1.1206.4.2.1.5.3.1.1`   | `1.3.6.1.4.1.1206.4.2.1.5.3.1.1.1`   | read-only      | 1                                                            |
| 161 | `timebaseAscPattern`               | column | `1.3.6.1.4.1.1206.4.2.1.5.3.1.2`   | `1.3.6.1.4.1.1206.4.2.1.5.3.1.2.1`   | read-write     | 255                                                          |
| 162 | `timebaseAscAuxillaryFunction`     | column | `1.3.6.1.4.1.1206.4.2.1.5.3.1.3`   | `1.3.6.1.4.1.1206.4.2.1.5.3.1.3.1`   | read-write     | 255                                                          |
| 163 | `timebaseAscSpecialFunction`       | column | `1.3.6.1.4.1.1206.4.2.1.5.3.1.4`   | `1.3.6.1.4.1.1206.4.2.1.5.3.1.4.1`   | read-write     | 255                                                          |
| 164 | `timebaseAscActionStatus`          | scalar | `1.3.6.1.4.1.1206.4.2.1.5.4`       | `1.3.6.1.4.1.1206.4.2.1.5.4.0`       | read-only      | 255                                                          |
| 165 | `preempt`                          | branch | `1.3.6.1.4.1.1206.4.2.1.6`         | `—`                                  | read-only      | —                                                            |
| 166 | `maxPreempts`                      | scalar | `1.3.6.1.4.1.1206.4.2.1.6.1`       | `1.3.6.1.4.1.1206.4.2.1.6.1.0`       | read-only      | 255                                                          |
| 167 | `preemptTable`                     | table  | `1.3.6.1.4.1.1206.4.2.1.6.2`       | `—`                                  | not-accessible | —                                                            |
| 168 | `preemptEntry`                     | entry  | `1.3.6.1.4.1.1206.4.2.1.6.2.1`     | `—`                                  | not-accessible | —                                                            |
| 169 | `preemptNumber`                    | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.1`   | `1.3.6.1.4.1.1206.4.2.1.6.2.1.1.1`   | read-only      | 1                                                            |
| 170 | `preemptDwellGreen`                | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.10`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.10.1`  | read-write     | 10                                                           |
| 171 | `preemptMaximumPresence`           | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.11`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.11.1`  | read-write     | 0                                                            |
| 172 | `preemptTrackPhase`                | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.12`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.12.1`  | read-write     | ""                                                           |
| 173 | `preemptDwellPhase`                | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.13`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.13.1`  | read-write     | ""                                                           |
| 174 | `preemptDwellPed`                  | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.14`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.14.1`  | read-write     | ""                                                           |
| 175 | `preemptExitPhase`                 | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.15`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.15.1`  | read-write     | ""                                                           |
| 176 | `preemptState`                     | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.16`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.16.1`  | read-only      | 9                                                            |
| 177 | `preemptTrackOverlap`              | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.17`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.17.1`  | read-write     | ""                                                           |
| 178 | `preemptDwellOverlap`              | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.18`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.18.1`  | read-write     | ""                                                           |
| 179 | `preemptCyclingPhase`              | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.19`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.19.1`  | read-write     | ""                                                           |
| 180 | `preemptControl`                   | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.2`   | `1.3.6.1.4.1.1206.4.2.1.6.2.1.2.1`   | read-write     | 0                                                            |
| 181 | `preemptCyclingPed`                | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.20`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.20.1`  | read-write     | ""                                                           |
| 182 | `preemptCyclingOverlap`            | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.21`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.21.1`  | read-write     | ""                                                           |
| 183 | `preemptEnterYellowChange`         | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.22`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.22.1`  | read-write     | 255                                                          |
| 184 | `preemptEnterRedClear`             | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.23`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.23.1`  | read-write     | 255                                                          |
| 185 | `preemptTrackYellowChange`         | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.24`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.24.1`  | read-write     | 255                                                          |
| 186 | `preemptTrackRedClear`             | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.25`  | `1.3.6.1.4.1.1206.4.2.1.6.2.1.25.1`  | read-write     | 255                                                          |
| 187 | `preemptLink`                      | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.3`   | `1.3.6.1.4.1.1206.4.2.1.6.2.1.3.1`   | read-write     | 0                                                            |
| 188 | `preemptDelay`                     | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.4`   | `1.3.6.1.4.1.1206.4.2.1.6.2.1.4.1`   | read-write     | 0                                                            |
| 189 | `preemptMinimumDuration`           | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.5`   | `1.3.6.1.4.1.1206.4.2.1.6.2.1.5.1`   | read-write     | 0                                                            |
| 190 | `preemptMinimumGreen`              | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.6`   | `1.3.6.1.4.1.1206.4.2.1.6.2.1.6.1`   | read-write     | 255                                                          |
| 191 | `preemptMinimumWalk`               | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.7`   | `1.3.6.1.4.1.1206.4.2.1.6.2.1.7.1`   | read-write     | 255                                                          |
| 192 | `preemptEnterPedClear`             | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.8`   | `1.3.6.1.4.1.1206.4.2.1.6.2.1.8.1`   | read-write     | 255                                                          |
| 193 | `preemptTrackGreen`                | column | `1.3.6.1.4.1.1206.4.2.1.6.2.1.9`   | `1.3.6.1.4.1.1206.4.2.1.6.2.1.9.1`   | read-write     | 0                                                            |
| 194 | `preemptControlTable`              | table  | `1.3.6.1.4.1.1206.4.2.1.6.3`       | `—`                                  | not-accessible | —                                                            |
| 195 | `preemptControlEntry`              | entry  | `1.3.6.1.4.1.1206.4.2.1.6.3.1`     | `—`                                  | not-accessible | —                                                            |
| 196 | `preemptControlNumber`             | column | `1.3.6.1.4.1.1206.4.2.1.6.3.1.1`   | `1.3.6.1.4.1.1206.4.2.1.6.3.1.1.1`   | read-only      | 1                                                            |
| 197 | `preemptControlState`              | column | `1.3.6.1.4.1.1206.4.2.1.6.3.1.2`   | `1.3.6.1.4.1.1206.4.2.1.6.3.1.2.1`   | read-write     | 1                                                            |
| 198 | `ring`                             | branch | `1.3.6.1.4.1.1206.4.2.1.7`         | `—`                                  | read-only      | —                                                            |
| 199 | `maxRings`                         | scalar | `1.3.6.1.4.1.1206.4.2.1.7.1`       | `1.3.6.1.4.1.1206.4.2.1.7.1.0`       | read-only      | 255                                                          |
| 200 | `maxSequences`                     | scalar | `1.3.6.1.4.1.1206.4.2.1.7.2`       | `1.3.6.1.4.1.1206.4.2.1.7.2.0`       | read-only      | 255                                                          |
| 201 | `sequenceTable`                    | table  | `1.3.6.1.4.1.1206.4.2.1.7.3`       | `—`                                  | not-accessible | —                                                            |
| 202 | `sequenceEntry`                    | entry  | `1.3.6.1.4.1.1206.4.2.1.7.3.1`     | `—`                                  | not-accessible | —                                                            |
| 203 | `sequenceNumber`                   | column | `1.3.6.1.4.1.1206.4.2.1.7.3.1.1`   | `1.3.6.1.4.1.1206.4.2.1.7.3.1.1.1.1` | read-only      | 1                                                            |
| 204 | `sequenceRingNumber`               | column | `1.3.6.1.4.1.1206.4.2.1.7.3.1.2`   | `1.3.6.1.4.1.1206.4.2.1.7.3.1.2.1.1` | read-only      | 1                                                            |
| 205 | `sequenceData`                     | column | `1.3.6.1.4.1.1206.4.2.1.7.3.1.3`   | `1.3.6.1.4.1.1206.4.2.1.7.3.1.3.1.1` | read-write     | 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ... (255 bytes) |
| 206 | `maxRingControlGroups`             | scalar | `1.3.6.1.4.1.1206.4.2.1.7.4`       | `1.3.6.1.4.1.1206.4.2.1.7.4.0`       | read-only      | 255                                                          |
| 207 | `ringControlGroupTable`            | table  | `1.3.6.1.4.1.1206.4.2.1.7.5`       | `—`                                  | not-accessible | —                                                            |
| 208 | `ringControlGroupEntry`            | entry  | `1.3.6.1.4.1.1206.4.2.1.7.5.1`     | `—`                                  | not-accessible | —                                                            |
| 209 | `ringControlGroupNumber`           | column | `1.3.6.1.4.1.1206.4.2.1.7.5.1.1`   | `1.3.6.1.4.1.1206.4.2.1.7.5.1.1.1`   | read-only      | 1                                                            |
| 210 | `ringControlGroupStopTime`         | column | `1.3.6.1.4.1.1206.4.2.1.7.5.1.2`   | `1.3.6.1.4.1.1206.4.2.1.7.5.1.2.1`   | read-write     | 255                                                          |
| 211 | `ringControlGroupForceOff`         | column | `1.3.6.1.4.1.1206.4.2.1.7.5.1.3`   | `1.3.6.1.4.1.1206.4.2.1.7.5.1.3.1`   | read-write     | 255                                                          |
| 212 | `ringControlGroupMax2`             | column | `1.3.6.1.4.1.1206.4.2.1.7.5.1.4`   | `1.3.6.1.4.1.1206.4.2.1.7.5.1.4.1`   | read-write     | 255                                                          |
| 213 | `ringControlGroupMaxInhibit`       | column | `1.3.6.1.4.1.1206.4.2.1.7.5.1.5`   | `1.3.6.1.4.1.1206.4.2.1.7.5.1.5.1`   | read-write     | 255                                                          |
| 214 | `ringControlGroupPedRecycle`       | column | `1.3.6.1.4.1.1206.4.2.1.7.5.1.6`   | `1.3.6.1.4.1.1206.4.2.1.7.5.1.6.1`   | read-write     | 255                                                          |
| 215 | `ringControlGroupRedRest`          | column | `1.3.6.1.4.1.1206.4.2.1.7.5.1.7`   | `1.3.6.1.4.1.1206.4.2.1.7.5.1.7.1`   | read-write     | 255                                                          |
| 216 | `ringControlGroupOmitRedClear`     | column | `1.3.6.1.4.1.1206.4.2.1.7.5.1.8`   | `1.3.6.1.4.1.1206.4.2.1.7.5.1.8.1`   | read-write     | 255                                                          |
| 217 | `ringStatusTable`                  | table  | `1.3.6.1.4.1.1206.4.2.1.7.6`       | `—`                                  | not-accessible | —                                                            |
| 218 | `ringStatusEntry`                  | entry  | `1.3.6.1.4.1.1206.4.2.1.7.6.1`     | `—`                                  | not-accessible | —                                                            |
| 219 | `ringStatus`                       | column | `1.3.6.1.4.1.1206.4.2.1.7.6.1.1`   | `1.3.6.1.4.1.1206.4.2.1.7.6.1.1.1`   | read-only      | 255                                                          |
| 220 | `channel`                          | branch | `1.3.6.1.4.1.1206.4.2.1.8`         | `—`                                  | read-only      | —                                                            |
| 221 | `maxChannels`                      | scalar | `1.3.6.1.4.1.1206.4.2.1.8.1`       | `1.3.6.1.4.1.1206.4.2.1.8.1.0`       | read-only      | 255                                                          |
| 222 | `channelTable`                     | table  | `1.3.6.1.4.1.1206.4.2.1.8.2`       | `—`                                  | not-accessible | —                                                            |
| 223 | `channelEntry`                     | entry  | `1.3.6.1.4.1.1206.4.2.1.8.2.1`     | `—`                                  | not-accessible | —                                                            |
| 224 | `channelNumber`                    | column | `1.3.6.1.4.1.1206.4.2.1.8.2.1.1`   | `1.3.6.1.4.1.1206.4.2.1.8.2.1.1.1`   | read-only      | 1                                                            |
| 225 | `channelControlSource`             | column | `1.3.6.1.4.1.1206.4.2.1.8.2.1.2`   | `1.3.6.1.4.1.1206.4.2.1.8.2.1.2.1`   | read-write     | 255                                                          |
| 226 | `channelControlType`               | column | `1.3.6.1.4.1.1206.4.2.1.8.2.1.3`   | `1.3.6.1.4.1.1206.4.2.1.8.2.1.3.1`   | read-write     | 4                                                            |
| 227 | `channelFlash`                     | column | `1.3.6.1.4.1.1206.4.2.1.8.2.1.4`   | `1.3.6.1.4.1.1206.4.2.1.8.2.1.4.1`   | read-write     | 255                                                          |
| 228 | `channelDim`                       | column | `1.3.6.1.4.1.1206.4.2.1.8.2.1.5`   | `1.3.6.1.4.1.1206.4.2.1.8.2.1.5.1`   | read-write     | 255                                                          |
| 229 | `maxChannelStatusGroups`           | scalar | `1.3.6.1.4.1.1206.4.2.1.8.3`       | `1.3.6.1.4.1.1206.4.2.1.8.3.0`       | read-only      | 255                                                          |
| 230 | `channelStatusGroupTable`          | table  | `1.3.6.1.4.1.1206.4.2.1.8.4`       | `—`                                  | not-accessible | —                                                            |
| 231 | `channelStatusGroupEntry`          | entry  | `1.3.6.1.4.1.1206.4.2.1.8.4.1`     | `—`                                  | not-accessible | —                                                            |
| 232 | `channelStatusGroupNumber`         | column | `1.3.6.1.4.1.1206.4.2.1.8.4.1.1`   | `1.3.6.1.4.1.1206.4.2.1.8.4.1.1.1`   | read-only      | 1                                                            |
| 233 | `channelStatusGroupReds`           | column | `1.3.6.1.4.1.1206.4.2.1.8.4.1.2`   | `1.3.6.1.4.1.1206.4.2.1.8.4.1.2.1`   | read-only      | 255                                                          |
| 234 | `channelStatusGroupYellows`        | column | `1.3.6.1.4.1.1206.4.2.1.8.4.1.3`   | `1.3.6.1.4.1.1206.4.2.1.8.4.1.3.1`   | read-only      | 255                                                          |
| 235 | `channelStatusGroupGreens`         | column | `1.3.6.1.4.1.1206.4.2.1.8.4.1.4`   | `1.3.6.1.4.1.1206.4.2.1.8.4.1.4.1`   | read-only      | 255                                                          |
| 236 | `overlap`                          | branch | `1.3.6.1.4.1.1206.4.2.1.9`         | `—`                                  | read-only      | —                                                            |
| 237 | `maxOverlaps`                      | scalar | `1.3.6.1.4.1.1206.4.2.1.9.1`       | `1.3.6.1.4.1.1206.4.2.1.9.1.0`       | read-only      | 255                                                          |
| 238 | `overlapTable`                     | table  | `1.3.6.1.4.1.1206.4.2.1.9.2`       | `—`                                  | not-accessible | —                                                            |
| 239 | `overlapEntry`                     | entry  | `1.3.6.1.4.1.1206.4.2.1.9.2.1`     | `—`                                  | not-accessible | —                                                            |
| 240 | `overlapNumber`                    | column | `1.3.6.1.4.1.1206.4.2.1.9.2.1.1`   | `1.3.6.1.4.1.1206.4.2.1.9.2.1.1.1`   | read-only      | 1                                                            |
| 241 | `overlapType`                      | column | `1.3.6.1.4.1.1206.4.2.1.9.2.1.2`   | `1.3.6.1.4.1.1206.4.2.1.9.2.1.2.1`   | read-only      | 3                                                            |
| 242 | `overlapIncludedPhases`            | column | `1.3.6.1.4.1.1206.4.2.1.9.2.1.3`   | `1.3.6.1.4.1.1206.4.2.1.9.2.1.3.1`   | read-write     | 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ... (255 bytes) |
| 243 | `overlapModifierPhases`            | column | `1.3.6.1.4.1.1206.4.2.1.9.2.1.4`   | `1.3.6.1.4.1.1206.4.2.1.9.2.1.4.1`   | read-write     | 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ... (255 bytes) |
| 244 | `overlapTrailGreen`                | column | `1.3.6.1.4.1.1206.4.2.1.9.2.1.5`   | `1.3.6.1.4.1.1206.4.2.1.9.2.1.5.1`   | read-write     | 255                                                          |
| 245 | `overlapTrailYellow`               | column | `1.3.6.1.4.1.1206.4.2.1.9.2.1.6`   | `1.3.6.1.4.1.1206.4.2.1.9.2.1.6.1`   | read-write     | 255                                                          |
| 246 | `overlapTrailRed`                  | column | `1.3.6.1.4.1.1206.4.2.1.9.2.1.7`   | `1.3.6.1.4.1.1206.4.2.1.9.2.1.7.1`   | read-write     | 255                                                          |
| 247 | `maxOverlapStatusGroups`           | scalar | `1.3.6.1.4.1.1206.4.2.1.9.3`       | `1.3.6.1.4.1.1206.4.2.1.9.3.0`       | read-only      | 255                                                          |
| 248 | `overlapStatusGroupTable`          | table  | `1.3.6.1.4.1.1206.4.2.1.9.4`       | `—`                                  | not-accessible | —                                                            |
| 249 | `overlapStatusGroupEntry`          | entry  | `1.3.6.1.4.1.1206.4.2.1.9.4.1`     | `—`                                  | not-accessible | —                                                            |
| 250 | `overlapStatusGroupNumber`         | column | `1.3.6.1.4.1.1206.4.2.1.9.4.1.1`   | `1.3.6.1.4.1.1206.4.2.1.9.4.1.1.1`   | read-only      | 1                                                            |
| 251 | `overlapStatusGroupReds`           | column | `1.3.6.1.4.1.1206.4.2.1.9.4.1.2`   | `1.3.6.1.4.1.1206.4.2.1.9.4.1.2.1`   | read-only      | 255                                                          |
| 252 | `overlapStatusGroupYellows`        | column | `1.3.6.1.4.1.1206.4.2.1.9.4.1.3`   | `1.3.6.1.4.1.1206.4.2.1.9.4.1.3.1`   | read-only      | 255                                                          |
| 253 | `overlapStatusGroupGreens`         | column | `1.3.6.1.4.1.1206.4.2.1.9.4.1.4`   | `1.3.6.1.4.1.1206.4.2.1.9.4.1.4.1`   | read-only      | 255                                                          |




## 说明

- **scalar**：实例 OID = 定义 OID + `.0`
- **column**：Get 列 OID（无行号）时，自动补 **table key 第 1 行**（如 `…8.2.1.1` → `…8.2.1.1.1`）；响应返回**完整实例 OID**
- **table/entry/branch**：`not-accessible`，无 SNMP 实例值
- 满填模式下每列另有 max* 行实例，完整树见 `tree/1202v0218-tree.md`

重新生成：`py scripts/gen_1202_defaults.py`