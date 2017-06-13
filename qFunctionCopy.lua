local function getModel(opt)
   local opt = opt or {}
   local envDetails = opt.envDetails
   local numTilings = opt.numTilings
   local numTiles = opt.numTiles
   local initialWeightVal = opt.initialWeightVal
   local traceType = opt.traceType
   local nbActions = envDetails.nbActions
   local memorySize = numTiles * numTiles
   local tc = require 'twrl.agent.model.tilecoding'({numTilings = numTilings, memorySize = memorySize}) 
   local weights = torch.FloatTensor((numTilings * memorySize) + 1):zero():fill(initialWeightVal)
   local eligibility = torch.FloatTensor((numTilings * memorySize) + 1):zero():fill(0)

   local function getFeatures(state, action)
      local floats = {}
      --print("1")
      o = 0.1
      for i = 1, envDetails.nbStates do
         print(o)
         o = i +1
         if envDetails.stateSpec.high[i] > 1000 then
            -- no scaling
            print("1.2")
            floats[i] = (numTilings * state[i]) / 1
         else
            -- scale to the max and min of the state space
            print("1.3")
            floats[i] = (numTilings * state[i]) / (envDetails.stateSpec.high[i] - envDetails.stateSpec.low[i])
         end
      end
      print("2")
      if envDetails.actionType == 'Discrete' then
         print("2.1")
         ints = {action}
      else
         print("2.2")
         table.insert(floats, action)
      end
      print("3")
      local features = tc.tiles(memorySize, numTilings, floats, ints)
      print("4")
      local featIdx = {}
      print("5")
      j = 0.7
      for tiling = 1, numTilings do
         print(j)
         j = j+1
         featIdx[tiling] = features[tiling] + ((tiling-1) * memorySize) + 1
      end
      -- add a baseline feature
      print("6")
      table.insert(featIdx, 1, 1)
      print("7")
      return featIdx
   end

   -- define accesory methods for the Q function
   local function estimateQ(state, action, w)
      -- estimate Q(s,a) as sum of corresponding weights
      local featIdx = getFeatures(state, action)
      local weightSum = 0
      for idx = 1, #featIdx do
         weightSum = weightSum + w[featIdx[idx]]      
      end
      return weightSum
   end

   local function estimateAllQ(state, w)
      -- estimate Q(s,a) for all actions
      local qVals = torch.Tensor(nbActions):zero()
      -- actions are base 0 for environment simplicity
      i = 0.1
      for action = 0, nbActions-1 do
         i = i + 1
         qVals[action+1] = estimateQ(state, action, w)
      end
      return qVals
   end
   
   local function accumulateEligibility(state, action, elig)
      local featIdx = getFeatures(state, action)
      -- accumulate eligibility for all features present in s,a
      for idx = 1, #featIdx do
         if traceType == 'replacing' then
            elig[featIdx[idx]] = 1
         elseif traceType == 'accumulating' then
            elig[featIdx[idx]] = elig[featIdx[idx]] + 1
         end
         eligibility = elig
      end
   end

   return { 
      weights = weights,
      eligibility = eligibility,
      accumulateEligibility = accumulateEligibility,
      estimateQ = estimateQ,
      estimateAllQ = estimateAllQ,
      getFeatures = getFeatures
   }
end
return getModel
