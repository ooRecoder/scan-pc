import unittest
from unittest.mock import patch, mock_open, MagicMock
from services.disk_service import DiskService  # use import absoluto

class TestDiskService(unittest.TestCase):
    @patch("psutil.disk_partitions")
    @patch("psutil.disk_usage")
    def test_collect_windows_ssd_hdd_removable(self, mock_disk_usage, mock_disk_partitions):
        # Mock de discos do sistema
        mock_disk_partitions.return_value = [
            MagicMock(device="C:", mountpoint="C:\\"),
            MagicMock(device="D:", mountpoint="D:\\"),
            MagicMock(device="E:", mountpoint="E:\\"),
        ]

        # Mock do uso do disco
        mock_disk_usage.return_value = MagicMock(
            total=500*(1024**3), used=200*(1024**3), free=300*(1024**3), percent=40
        )

        service = DiskService()

        # Forçar plataforma Windows
        with patch("platform.system", return_value="Windows"):
            # Mock do subprocess.check_output para retornar tipos de disco
            with patch("subprocess.check_output") as mock_check_output:
                mock_check_output.return_value = (
                    "DeviceID  MediaType\n"
                    "C: SSD\n"
                    "D: HDD\n"
                    "E: REMOVABLE\n"
                )

                result = service.collect()

                # Mostrar retorno no console
                print("\nRetorno de collect():", result)

                # Asserções
                self.assertEqual(result["Discos"]["C:"]["Tipo"], "SSD")
                self.assertEqual(result["Discos"]["D:"]["Tipo"], "HDD")
                self.assertEqual(result["Discos"]["E:"]["Tipo"], "Pendrive/Removível")

if __name__ == "__main__":
    unittest.main()
