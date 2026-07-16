# 1202 全部对象清单（SET 版）

> **版本标注 SET** — 在 `1202DEFAULT_DATA-OIDs.md`（Get/默认值）基础上增加 Set 测试结果

| 项 | 值 |
|---|---|
| 生成时间 | 2026-07-08 02:21 UTC |
| SET 自测 | **PASS** |
| dev_cap | 8 |
| 可写对象数 | 137 |

## Set 测试说明

- **read-write**：进程内 Set → Get 读回 + 非法值拒绝
- **read-only / not-accessible**：Set 拒绝
- 重启 Agent 后恢复默认（方案 A，不做持久化）

## 可写对象 Set 结果

| # | 对象名 | 实例 OID | Set 读回 | 说明 |
|---|---|---|---|---|
| 1 | `ascBlockData` | `1.3.6.1.4.1.1206.4.2.1.11.2.0` | PASS | invalid Set rejected |
| 2 | `ascBlockGetControl` | `1.3.6.1.4.1.1206.4.2.1.11.1.0` | PASS | invalid Set rejected |
| 3 | `auxIOPortDescription` | `1.3.6.1.4.1.1206.4.2.6.7.3.1.3.2.1` | PASS | invalid Set rejected |
| 4 | `auxIOPortValue` | `1.3.6.1.4.1.1206.4.2.6.7.3.1.5.2.1` | PASS | invalid Set rejected |
| 5 | `channelControlSource` | `1.3.6.1.4.1.1206.4.2.1.8.2.1.2.1` | PASS | invalid Set rejected |
| 6 | `channelControlType` | `1.3.6.1.4.1.1206.4.2.1.8.2.1.3.1` | PASS | invalid Set rejected |
| 7 | `channelDim` | `1.3.6.1.4.1.1206.4.2.1.8.2.1.5.1` | PASS | invalid Set rejected |
| 8 | `channelFlash` | `1.3.6.1.4.1.1206.4.2.1.8.2.1.4.1` | PASS | invalid Set rejected |
| 9 | `communityNameAccessMask` | `1.3.6.1.4.1.1206.4.2.6.5.3.1.3.1` | PASS | invalid Set rejected |
| 10 | `communityNameAdmin` | `1.3.6.1.4.1.1206.4.2.6.5.1.0` | PASS | invalid Set rejected |
| 11 | `communityNameUser` | `1.3.6.1.4.1.1206.4.2.6.5.3.1.2.1` | PASS | invalid Set rejected |
| 12 | `controllerStandardTimeZone` | `1.3.6.1.4.1.1206.4.2.6.3.5.0` | PASS | invalid Set rejected |
| 13 | `coordCorrectionMode` | `1.3.6.1.4.1.1206.4.2.1.4.2.0` | PASS | invalid Set rejected |
| 14 | `coordForceMode` | `1.3.6.1.4.1.1206.4.2.1.4.4.0` | PASS | invalid Set rejected |
| 15 | `coordMaximumMode` | `1.3.6.1.4.1.1206.4.2.1.4.3.0` | PASS | invalid Set rejected |
| 16 | `coordOperationalMode` | `1.3.6.1.4.1.1206.4.2.1.4.1.0` | PASS | invalid Set rejected |
| 17 | `dayPlanActionNumberOID` | `1.3.6.1.4.1.1206.4.2.6.3.3.5.1.5.1.1` | PASS | invalid Set rejected |
| 18 | `dayPlanHour` | `1.3.6.1.4.1.1206.4.2.6.3.3.5.1.3.1.1` | PASS | invalid Set rejected |
| 19 | `dayPlanMinute` | `1.3.6.1.4.1.1206.4.2.6.3.3.5.1.4.1.1` | PASS | invalid Set rejected |
| 20 | `dbCreateTransaction` | `1.3.6.1.4.1.1206.4.2.6.2.1.0` | PASS | invalid Set rejected |
| 21 | `eventClassClearTime` | `1.3.6.1.4.1.1206.4.2.6.4.6.1.3.1` | PASS | invalid Set rejected |
| 22 | `eventClassDescription` | `1.3.6.1.4.1.1206.4.2.6.4.6.1.4.1` | PASS | invalid Set rejected |
| 23 | `eventClassLimit` | `1.3.6.1.4.1.1206.4.2.6.4.6.1.2.1` | PASS | invalid Set rejected |
| 24 | `eventConfigAction` | `1.3.6.1.4.1.1206.4.2.6.4.2.1.8.1` | PASS | invalid Set rejected |
| 25 | `eventConfigClass` | `1.3.6.1.4.1.1206.4.2.6.4.2.1.2.1` | PASS | invalid Set rejected |
| 26 | `eventConfigCompareOID` | `1.3.6.1.4.1.1206.4.2.6.4.2.1.6.1` | PASS | invalid Set rejected |
| 27 | `eventConfigCompareValue` | `1.3.6.1.4.1.1206.4.2.6.4.2.1.4.1` | PASS | invalid Set rejected |
| 28 | `eventConfigCompareValue2` | `1.3.6.1.4.1.1206.4.2.6.4.2.1.5.1` | PASS | invalid Set rejected |
| 29 | `eventConfigLogOID` | `1.3.6.1.4.1.1206.4.2.6.4.2.1.7.1` | PASS | invalid Set rejected |
| 30 | `eventConfigMode` | `1.3.6.1.4.1.1206.4.2.6.4.2.1.3.1` | PASS | invalid Set rejected |
| 31 | `globalDaylightSaving` | `1.3.6.1.4.1.1206.4.2.6.3.2.0` | PASS | invalid Set rejected |
| 32 | `globalTime` | `1.3.6.1.4.1.1206.4.2.6.3.1.0` | PASS | invalid Set rejected |
| 33 | `overlapIncludedPhases` | `1.3.6.1.4.1.1206.4.2.1.9.2.1.3.1` | PASS | invalid Set rejected |
| 34 | `overlapModifierPhases` | `1.3.6.1.4.1.1206.4.2.1.9.2.1.4.1` | PASS | invalid Set rejected |
| 35 | `overlapTrailGreen` | `1.3.6.1.4.1.1206.4.2.1.9.2.1.5.1` | PASS | invalid Set rejected |
| 36 | `overlapTrailRed` | `1.3.6.1.4.1.1206.4.2.1.9.2.1.7.1` | PASS | invalid Set rejected |
| 37 | `overlapTrailYellow` | `1.3.6.1.4.1.1206.4.2.1.9.2.1.6.1` | PASS | invalid Set rejected |
| 38 | `patternCycleTime` | `1.3.6.1.4.1.1206.4.2.1.4.7.1.2.1` | PASS | invalid Set rejected |
| 39 | `patternOffsetTime` | `1.3.6.1.4.1.1206.4.2.1.4.7.1.3.1` | PASS | invalid Set rejected |
| 40 | `patternSequenceNumber` | `1.3.6.1.4.1.1206.4.2.1.4.7.1.5.1` | PASS | invalid Set rejected |
| 41 | `pedestrianDetectorCallPhase` | `1.3.6.1.4.1.1206.4.2.1.2.7.1.2.1` | PASS | invalid Set rejected |
| 42 | `pedestrianDetectorErraticCounts` | `1.3.6.1.4.1.1206.4.2.1.2.7.1.5.1` | PASS | invalid Set rejected |
| 43 | `pedestrianDetectorMaxPresence` | `1.3.6.1.4.1.1206.4.2.1.2.7.1.4.1` | PASS | invalid Set rejected |
| 44 | `pedestrianDetectorNoActivity` | `1.3.6.1.4.1.1206.4.2.1.2.7.1.3.1` | PASS | invalid Set rejected |
| 45 | `phaseAddedInitial` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.11.1` | PASS | invalid Set rejected |
| 46 | `phaseCarsBeforeReduction` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.14.1` | PASS | invalid Set rejected |
| 47 | `phaseConcurrency` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.23.1` | PASS | invalid Set rejected |
| 48 | `phaseControlGroupForceOff` | `1.3.6.1.4.1.1206.4.2.1.1.5.1.5.1` | PASS | invalid Set rejected |
| 49 | `phaseControlGroupHold` | `1.3.6.1.4.1.1206.4.2.1.1.5.1.4.1` | PASS | invalid Set rejected |
| 50 | `phaseControlGroupPedCall` | `1.3.6.1.4.1.1206.4.2.1.1.5.1.7.1` | PASS | invalid Set rejected |
| 51 | `phaseControlGroupPedOmit` | `1.3.6.1.4.1.1206.4.2.1.1.5.1.3.1` | PASS | invalid Set rejected |
| 52 | `phaseControlGroupPhaseOmit` | `1.3.6.1.4.1.1206.4.2.1.1.5.1.2.1` | PASS | invalid Set rejected |
| 53 | `phaseControlGroupVehCall` | `1.3.6.1.4.1.1206.4.2.1.1.5.1.6.1` | PASS | invalid Set rejected |
| 54 | `phaseDynamicMaxLimit` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.18.1` | PASS | invalid Set rejected |
| 55 | `phaseDynamicMaxStep` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.19.1` | PASS | invalid Set rejected |
| 56 | `phaseMaximum1` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.6.1` | PASS | invalid Set rejected |
| 57 | `phaseMaximum2` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.7.1` | PASS | invalid Set rejected |
| 58 | `phaseMaximumInitial` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.12.1` | PASS | invalid Set rejected |
| 59 | `phaseMinimumGap` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.17.1` | PASS | invalid Set rejected |
| 60 | `phaseMinimumGreen` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.4.1` | PASS | invalid Set rejected |
| 61 | `phaseOptions` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.21.1` | PASS | invalid Set rejected |
| 62 | `phasePassage` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.5.1` | PASS | invalid Set rejected |
| 63 | `phasePedestrianClear` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.3.1` | PASS | invalid Set rejected |
| 64 | `phaseRedClear` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.9.1` | PASS | invalid Set rejected |
| 65 | `phaseRedRevert` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.10.1` | PASS | invalid Set rejected |
| 66 | `phaseReduceBy` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.16.1` | PASS | invalid Set rejected |
| 67 | `phaseRing` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.22.1` | PASS | invalid Set rejected |
| 68 | `phaseStartup` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.20.1` | PASS | invalid Set rejected |
| 69 | `phaseTimeBeforeReduction` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.13.1` | PASS | invalid Set rejected |
| 70 | `phaseTimeToReduce` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.15.1` | PASS | invalid Set rejected |
| 71 | `phaseWalk` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.2.1` | PASS | invalid Set rejected |
| 72 | `phaseYellowChange` | `1.3.6.1.4.1.1206.4.2.1.1.2.1.8.1` | PASS | invalid Set rejected |
| 73 | `port1DevicePresent` | `1.3.6.1.4.1.1206.4.2.1.10.2.1.2.1` | PASS | invalid Set rejected |
| 74 | `port1Frame40Enable` | `1.3.6.1.4.1.1206.4.2.1.10.2.1.3.1` | PASS | invalid Set rejected |
| 75 | `preemptControl` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.2.1` | PASS | invalid Set rejected |
| 76 | `preemptControlState` | `1.3.6.1.4.1.1206.4.2.1.6.3.1.2.1` | PASS | invalid Set rejected |
| 77 | `preemptCyclingOverlap` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.21.1` | PASS | invalid Set rejected |
| 78 | `preemptCyclingPed` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.20.1` | PASS | invalid Set rejected |
| 79 | `preemptCyclingPhase` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.19.1` | PASS | invalid Set rejected |
| 80 | `preemptDelay` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.4.1` | PASS | invalid Set rejected |
| 81 | `preemptDwellGreen` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.10.1` | PASS | invalid Set rejected |
| 82 | `preemptDwellOverlap` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.18.1` | PASS | invalid Set rejected |
| 83 | `preemptDwellPed` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.14.1` | PASS | invalid Set rejected |
| 84 | `preemptDwellPhase` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.13.1` | PASS | invalid Set rejected |
| 85 | `preemptEnterPedClear` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.8.1` | PASS | invalid Set rejected |
| 86 | `preemptEnterRedClear` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.23.1` | PASS | invalid Set rejected |
| 87 | `preemptEnterYellowChange` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.22.1` | PASS | invalid Set rejected |
| 88 | `preemptExitPhase` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.15.1` | PASS | invalid Set rejected |
| 89 | `preemptLink` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.3.1` | PASS | invalid Set rejected |
| 90 | `preemptMaximumPresence` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.11.1` | PASS | invalid Set rejected |
| 91 | `preemptMinimumDuration` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.5.1` | PASS | invalid Set rejected |
| 92 | `preemptMinimumGreen` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.6.1` | PASS | invalid Set rejected |
| 93 | `preemptMinimumWalk` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.7.1` | PASS | invalid Set rejected |
| 94 | `preemptTrackGreen` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.9.1` | PASS | invalid Set rejected |
| 95 | `preemptTrackOverlap` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.17.1` | PASS | invalid Set rejected |
| 96 | `preemptTrackPhase` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.12.1` | PASS | invalid Set rejected |
| 97 | `preemptTrackRedClear` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.25.1` | PASS | invalid Set rejected |
| 98 | `preemptTrackYellowChange` | `1.3.6.1.4.1.1206.4.2.1.6.2.1.24.1` | PASS | invalid Set rejected |
| 99 | `ringControlGroupForceOff` | `1.3.6.1.4.1.1206.4.2.1.7.5.1.3.1` | PASS | invalid Set rejected |
| 100 | `ringControlGroupMax2` | `1.3.6.1.4.1.1206.4.2.1.7.5.1.4.1` | PASS | invalid Set rejected |
| 101 | `ringControlGroupMaxInhibit` | `1.3.6.1.4.1.1206.4.2.1.7.5.1.5.1` | PASS | invalid Set rejected |
| 102 | `ringControlGroupOmitRedClear` | `1.3.6.1.4.1.1206.4.2.1.7.5.1.8.1` | PASS | invalid Set rejected |
| 103 | `ringControlGroupPedRecycle` | `1.3.6.1.4.1.1206.4.2.1.7.5.1.6.1` | PASS | invalid Set rejected |
| 104 | `ringControlGroupRedRest` | `1.3.6.1.4.1.1206.4.2.1.7.5.1.7.1` | PASS | invalid Set rejected |
| 105 | `ringControlGroupStopTime` | `1.3.6.1.4.1.1206.4.2.1.7.5.1.2.1` | PASS | invalid Set rejected |
| 106 | `sequenceData` | `1.3.6.1.4.1.1206.4.2.1.7.3.1.3.1.1` | PASS | invalid Set rejected |
| 107 | `specialFunctionOutputControl` | `1.3.6.1.4.1.1206.4.2.1.3.14.1.3.1` | PASS | invalid Set rejected |
| 108 | `splitCoordPhase` | `1.3.6.1.4.1.1206.4.2.1.4.9.1.5.1.1` | PASS | invalid Set rejected |
| 109 | `splitMode` | `1.3.6.1.4.1.1206.4.2.1.4.9.1.4.1.1` | PASS | invalid Set rejected |
| 110 | `splitTime` | `1.3.6.1.4.1.1206.4.2.1.4.9.1.3.1.1` | PASS | invalid Set rejected |
| 111 | `systemPatternControl` | `1.3.6.1.4.1.1206.4.2.1.4.14.0` | PASS | invalid Set rejected |
| 112 | `systemSyncControl` | `1.3.6.1.4.1.1206.4.2.1.4.15.0` | PASS | invalid Set rejected |
| 113 | `timeBaseScheduleDate` | `1.3.6.1.4.1.1206.4.2.6.3.3.2.1.4.1` | PASS | invalid Set rejected |
| 114 | `timeBaseScheduleDay` | `1.3.6.1.4.1.1206.4.2.6.3.3.2.1.3.1` | PASS | invalid Set rejected |
| 115 | `timeBaseScheduleDayPlan` | `1.3.6.1.4.1.1206.4.2.6.3.3.2.1.5.1` | PASS | invalid Set rejected |
| 116 | `timeBaseScheduleMonth` | `1.3.6.1.4.1.1206.4.2.6.3.3.2.1.2.1` | PASS | invalid Set rejected |
| 117 | `timebaseAscAuxillaryFunction` | `1.3.6.1.4.1.1206.4.2.1.5.3.1.3.1` | PASS | invalid Set rejected |
| 118 | `timebaseAscPattern` | `1.3.6.1.4.1.1206.4.2.1.5.3.1.2.1` | PASS | invalid Set rejected |
| 119 | `timebaseAscPatternSync` | `1.3.6.1.4.1.1206.4.2.1.5.1.0` | PASS | invalid Set rejected |
| 120 | `timebaseAscSpecialFunction` | `1.3.6.1.4.1.1206.4.2.1.5.3.1.4.1` | PASS | invalid Set rejected |
| 121 | `unitAutoPedestrianClear` | `1.3.6.1.4.1.1206.4.2.1.3.2.0` | PASS | invalid Set rejected |
| 122 | `unitBackupTime` | `1.3.6.1.4.1.1206.4.2.1.3.3.0` | PASS | invalid Set rejected |
| 123 | `unitControl` | `1.3.6.1.4.1.1206.4.2.1.3.10.0` | PASS | invalid Set rejected |
| 124 | `unitRedRevert` | `1.3.6.1.4.1.1206.4.2.1.3.4.0` | PASS | invalid Set rejected |
| 125 | `unitStartUpFlash` | `1.3.6.1.4.1.1206.4.2.1.3.1.0` | PASS | invalid Set rejected |
| 126 | `vehicleDetectorCallPhase` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.4.1` | PASS | invalid Set rejected |
| 127 | `vehicleDetectorDelay` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.6.1` | PASS | invalid Set rejected |
| 128 | `vehicleDetectorErraticCounts` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.11.1` | PASS | invalid Set rejected |
| 129 | `vehicleDetectorExtend` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.7.1` | PASS | invalid Set rejected |
| 130 | `vehicleDetectorFailTime` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.12.1` | PASS | invalid Set rejected |
| 131 | `vehicleDetectorMaxPresence` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.10.1` | PASS | invalid Set rejected |
| 132 | `vehicleDetectorNoActivity` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.9.1` | PASS | invalid Set rejected |
| 133 | `vehicleDetectorOptions` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.2.1` | PASS | invalid Set rejected |
| 134 | `vehicleDetectorQueueLimit` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.8.1` | PASS | invalid Set rejected |
| 135 | `vehicleDetectorReset` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.15.1` | PASS | invalid Set rejected |
| 136 | `vehicleDetectorSwitchPhase` | `1.3.6.1.4.1.1206.4.2.1.2.2.1.5.1` | PASS | invalid Set rejected |
| 137 | `volumeOccupancyPeriod` | `1.3.6.1.4.1.1206.4.2.1.2.5.2.0` | PASS | invalid Set rejected |

完整默认值见 [1202DEFAULT_DATA-OIDs.md](1202DEFAULT_DATA-OIDs.md)。

重新生成：

```bash
py scripts/selftest_1202_set.py
```