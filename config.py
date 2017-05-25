
#TEST_GLOBAL_PARAMETERS_PATH="testGlobalParameters.properties"
#RELEASE_GLOBAL_PARAMETERS="releaseGlobalParameters.properties"

class Config: 

	def createTestGlobalConfiguration():
		
		testGlobalConfiguration=dict()

		#markers (in meters)
		testGlobalConfiguration["MARKERS_WIDTH"] = 32 * 10**(-2) 
		testGlobalConfiguration["MARKERS_HEIGHT"] = 32 * 10**(-2)
		testGlobalConfiguration["SUPPOSED_FPS"] = 30

		#masks
		testGlobalConfiguration["GREEN_LOWER"] = (23, 23, 102)
		testGlobalConfiguration["GREEN_UPPER"] = (100, 100, 250)
		testGlobalConfiguration["CYAN_LOWER"] = (23, 50, 100)
		testGlobalConfiguration["CYAN_UPPER"] = (200, 255, 255)

		return testGlobalConfiguration

	def createReleaseGlobalConfiguration():
		
		testGlobalConfiguration=dict()

		#markers (in meters)
		testGlobalConfiguration["MARKERS_WIDTH"] = 32 * 10**(-2) 
		testGlobalConfiguration["MARKERS_HEIGHT"] = 32 * 10**(-2)
		testGlobalConfiguration["SUPPOSED_FPS"] = 30

		#masks
		testGlobalConfiguration["GREEN_LOWER"] = (23, 23, 102)
		testGlobalConfiguration["GREEN_UPPER"] = (100, 100, 250)
		testGlobalConfiguration["CYAN_LOWER"] = (23, 50, 100)
		testGlobalConfiguration["CYAN_UPPER"] = (200, 255, 255)

		return testGlobalConfiguration
