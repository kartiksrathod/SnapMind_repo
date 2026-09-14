from dataclasses import asdict, dataclass
import os
import platform
import subprocess


@dataclass(frozen=True)
class DeviceCapability:
    name: str
    status: str
    evidence: str
    limitation: str | None = None


@dataclass(frozen=True)
class HardwareCapabilities:
    os: str
    processor: str
    cpu: DeviceCapability
    gpu: DeviceCapability
    npu: DeviceCapability

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _windows_gpu() -> str | None:
    if platform.system() != 'Windows':
        return None
    try:
        result = subprocess.run(
            ['powershell', '-NoProfile', '-Command', 'Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name'],
            capture_output=True, text=True, timeout=3, check=True,
        )
        names = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return ', '.join(names) if names else None
    except (OSError, subprocess.SubprocessError):
        return None


def detect_hardware() -> HardwareCapabilities:
    processor = platform.processor() or platform.machine() or 'Unknown processor'
    gpu_name = _windows_gpu()
    cpu = DeviceCapability('CPU', 'available', f'Python platform reports {processor}; {os.cpu_count() or "unknown"} logical processors.')
    gpu = DeviceCapability('GPU', 'available' if gpu_name else 'unknown', f'Windows reports {gpu_name}.' if gpu_name else 'GPU information could not be queried.')
    npu = DeviceCapability('NPU', 'unknown', 'NPU execution not verified', 'No Qualcomm/NPU device or supported runtime was detected in this environment.')
    return HardwareCapabilities(
        os=f'{platform.system()} {platform.release()}', processor=processor, cpu=cpu, gpu=gpu, npu=npu,
    )
