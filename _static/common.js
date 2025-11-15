/* === common.js (共通スクリプト) === */

/* 即時関数で囲み、グローバル汚染を防ぐ */
(function() {
  
  /* === 1. 進捗タブの切り替え (変更なし) === */
  const tabRole2 = document.getElementById('tab-role2');
  const tabRole1 = document.getElementById('tab-role1');
  const stepsRole2 = document.getElementById('steps-role2');
  const stepsRole1 = document.getElementById('steps-role1');

  if (tabRole2 && tabRole1 && stepsRole2 && stepsRole1) {
    tabRole2.addEventListener('click', function() {
      tabRole2.classList.add('active');
      tabRole1.classList.remove('active');
      stepsRole2.classList.add('active');
      stepsRole1.classList.remove('active');
    });

    tabRole1.addEventListener('click', function() {
      tabRole1.classList.add('active');
      tabRole2.classList.remove('active');
      stepsRole1.classList.add('active');
      stepsRole2.classList.remove('active');
    });
  }
  
  /* === 2. ルール確認ポップアップ (モーダル) (変更なし) === */
  const rulesModal = document.getElementById('rules-modal');
  const openRulesBtn = document.getElementById('open-rules-modal');
  const closeRulesBtn = document.getElementById('close-rules-modal');

  if (rulesModal && openRulesBtn && closeRulesBtn) {
    openRulesBtn.addEventListener('click', function() {
      rulesModal.style.display = 'flex';
    });
    closeRulesBtn.addEventListener('click', function() {
      rulesModal.style.display = 'none';
    });
    rulesModal.addEventListener('click', function(event) {
      if (event.target === rulesModal) {
        rulesModal.style.display = 'none';
      }
    });
  }

  /* === 3. 中断リンク (変更なし) === */
  const quitLink = document.getElementById('quit-link');
  if (quitLink) {
    quitLink.addEventListener('click', function() {
      console.log('中断がクリックされました。');
    });
  }

  /* === 4. 汎用カードデッキUIコントローラー (P11用) (変更なし) === */
  window.CardDeckController = (function() {
    let wrapperEl = null;
    let cardTemplateHTML = '';
    let maxTrials = 0;
    let currentTrialIndex = 0;
    let cardElements = [];
    let onCardSetupCallback = null;
    let onNextCallback = null;

    function updateDeckView() {
      cardElements.forEach((card, index) => {
        card.classList.remove('is-active', 'is-next', 'is-stacked', 'is-gone');
        if (index < currentTrialIndex) {
          card.classList.add('is-gone');
        } else if (index === currentTrialIndex) {
          card.classList.add('is-active');
        } else if (index === currentTrialIndex + 1) {
          card.classList.add('is-next');
        } else {
          card.classList.add('is-stacked');
        }
      });
    }

    function handleNextClick() {
      if (currentTrialIndex >= maxTrials) return;
      const activeCard = cardElements[currentTrialIndex];
      if (onNextCallback) {
        onNextCallback(activeCard);
      }
      currentTrialIndex++;
      updateDeckView();
    }

    function createCards() {
      wrapperEl.innerHTML = '';
      cardElements = [];
      for (let i = 0; i < maxTrials; i++) {
        const cardDiv = document.createElement('div');
        cardDiv.innerHTML = cardTemplateHTML;
        const cardEl = cardDiv.firstElementChild;
        cardEl.classList.add('deck-card');
        cardEl.dataset.trial = i + 1;
        cardEl.querySelector('.trial-current').textContent = i + 1;
        cardEl.querySelector('.trial-max').textContent = maxTrials;
        const nextButton = cardEl.querySelector('.btn-deck-next');
        if (nextButton) {
          nextButton.addEventListener('click', handleNextClick);
        }
        wrapperEl.appendChild(cardEl);
        cardElements.push(cardEl);
        if (onCardSetupCallback) {
          onCardSetupCallback(cardEl);
        }
      }
    }

    return {
      init: function(wrapperSelector, setupCallback, nextCallback) {
        wrapperEl = document.querySelector(wrapperSelector);
        if (!wrapperEl) { console.error('CardDeck ラッパーが見つかりません:', wrapperSelector); return; }
        const template = wrapperEl.querySelector('.deck-card-template');
        if (!template) { console.error('deck-card-template が見つかりません。'); return; }
        cardTemplateHTML = template.innerHTML;
        template.remove();
        maxTrials = parseInt(wrapperEl.dataset.maxTrials) || 1;
        onCardSetupCallback = setupCallback;
        onNextCallback = nextCallback;
        this.reset();
      },
      reset: function() {
        currentTrialIndex = 0;
        createCards();
        updateDeckView();
      }
    };
  })();

  /* === 5. 汎用スライダー連動関数 (P12, P14用) (変更なし) === */
  /**
   * スライダーとその隣の数値を同期させる汎用関数
   * @param {string} sliderSelector - 対象スライダーのCSSセレクタ (例: '.invest-slider')
   * @param {string} valueDisplaySelector - 数値表示用spanのCSSセレクタ (例: '.slider-value')
   */
  window.setupSliderSync = function(sliderSelector, valueDisplaySelector) {
    document.querySelectorAll(sliderSelector).forEach(slider => {
      const container = slider.closest('.slider-container');
      if (!container) return;
      const valueDisplay = container.querySelector(valueDisplaySelector);
      if (!valueDisplay) return;
      valueDisplay.textContent = slider.value;
      slider.addEventListener('input', () => {
        valueDisplay.textContent = slider.value;
      });
    });
  };

  /* === 6. 汎用ドラッグ＆ドロップ(D&D)コントローラー (P14用) (変更なし) === */
  /**
   * 優先順位付けD&Dを管理するコントローラー
   * @param {string} draggableSelector - ドラッグ対象のCSSセレクタ (例: '.draggable')
   * @param {string} dropzoneSelector - ドロップ先(枠)のCSSセレクタ (例: '.dropzone')
   * @param {string} originContainerSelector - ドラッグ元のコンテナ (例: '#draggable-container')
   */
  window.DragDropController = (function() {
    let draggables = [];
    let dropzones = [];
    let originContainer = null;
    let draggedItem = null;
    
    const state = {
      ranks: {},
      isComplete: function() {
        return draggables.length === Object.keys(this.ranks).length;
      }
    };

    function onDragStart(e) {
      draggedItem = e.target;
      setTimeout(() => e.target.classList.add('is-dragging'), 0);
    }
    function onDragEnd(e) {
      e.target.classList.remove('is-dragging');
      draggedItem = null;
    }
    function onDragOver(e) {
      e.preventDefault();
      const zone = e.target.closest(dropzones.selector);
      if (zone) zone.classList.add('is-over');
    }
    function onDragLeave(e) {
      const zone = e.target.closest(dropzones.selector);
      if (zone) zone.classList.remove('is-over');
    }
    function onDrop(e) {
      e.preventDefault();
      if (!draggedItem) return;
      const dropTarget = e.target.closest(dropzones.selector) || originContainer;
      dropTarget.classList.remove('is-over');
      const existingItem = dropTarget.querySelector(draggables.selector);
      if (existingItem && existingItem !== draggedItem) {
        originContainer.appendChild(existingItem);
        existingItem.closest('.dropzone')?.classList.remove('is-filled');
      }
      dropTarget.appendChild(draggedItem);
      updateRanksState();
    }
    function updateRanksState() {
      state.ranks = {};
      dropzones.forEach(zone => {
        const item = zone.querySelector(draggables.selector);
        if (item) {
          const rank = zone.dataset.rank;
          const playerId = item.dataset.playerId;
          state.ranks[rank] = playerId;
          zone.classList.add('is-filled');
        } else {
          zone.classList.remove('is-filled');
        }
      });
    }

    return {
      init: function(draggableSelector, dropzoneSelector, originContainerSelector) {
        draggables = Array.from(document.querySelectorAll(draggableSelector));
        dropzones = Array.from(document.querySelectorAll(dropzoneSelector));
        originContainer = document.querySelector(originContainerSelector);
        draggables.selector = draggableSelector;
        dropzones.selector = dropzoneSelector;
        if (!originContainer) { console.error('D&Dのドラッグ元コンテナが見つかりません:', originContainerSelector); return; }
        draggables.forEach(item => {
          item.addEventListener('dragstart', onDragStart);
          item.addEventListener('dragend', onDragEnd);
        });
        dropzones.forEach(zone => {
          zone.addEventListener('dragover', onDragOver);
          zone.addEventListener('dragleave', onDragLeave);
          zone.addEventListener('drop', onDrop);
        });
        originContainer.addEventListener('dragover', onDragOver);
        originContainer.addEventListener('dragleave', onDragLeave);
        originContainer.addEventListener('drop', onDrop);
      },
      reset: function() {
        dropzones.forEach(zone => {
          const item = zone.querySelector(draggables.selector);
          if (item) originContainer.appendChild(item);
        });
        updateRanksState();
      },
      getState: function() {
        return state;
      }
    };
  })();


  /* === 7. ★ 新規追加: 汎用フォームバリデーション (P15用) === */
  /**
   * フォーム内の必須項目を検証する汎用関数
   * @param {HTMLElement} formElement - 検証対象の <form> 要素
   * @returns {boolean} - バリデーションが成功したかどうか
   */
  window.validateForm = function(formElement) {
    if (!formElement) return false;

    let isValid = true;
    // すべての .question-block を取得
    const questions = formElement.querySelectorAll('.question-block');

    questions.forEach(block => {
      let blockIsValid = false;
      
      // 1. ラジオボタン (リッカート尺度、名義尺度) のチェック
      // data-question-name 属性を持つコンテナ（.likert-scale-7 など）を探す
      const radioGroups = block.querySelectorAll('[data-question-name]');
      if (radioGroups.length > 0) {
        // グループごとにチェック
        let allGroupsValid = true;
        radioGroups.forEach(group => {
          const groupName = group.dataset.questionName;
          if (!formElement.querySelector(`input[name="${groupName}"]:checked`)) {
            allGroupsValid = false;
          }
        });
        blockIsValid = allGroupsValid;
      }
      
      // 2. 名義尺度 (data-question-name を使わない単純なラジオ) のチェック
      const simpleRadios = block.querySelectorAll('input[type="radio"]');
      if (!blockIsValid && radioGroups.length === 0 && simpleRadios.length > 0) {
        if (block.querySelector('input[type="radio"]:checked')) {
          blockIsValid = true;
        }
      }

      // 3. 数値入力・テキスト入力のチェック
      const numberInput = block.querySelector('input[type="number"], input[type="text"]');
      if (!blockIsValid && numberInput) {
        if (numberInput.value.trim() !== '') {
          blockIsValid = true;
        }
      }
      
      // 4. スライダー入力 (range) のチェック
      // スライダーは初期値が必ずあるため、必須チェックは通常不要。
      // もし特定のデフォルト値（例: 50）以外を必須とするならロジック追加。
      // ここではスライダーは常に「回答済み」とみなす。
      const rangeInput = block.querySelector('input[type="range"]');
      if (!blockIsValid && rangeInput) {
        blockIsValid = true; // スライダーは常に有効とみなす
      }

      // 最終判定
      if (blockIsValid) {
        block.classList.remove('question-error');
      } else {
        block.classList.add('question-error');
        isValid = false; // 1つでも無効なブロックがあれば、フォーム全体が無効
      }
    });

    return isValid;
  };


})(); // 全体の即時関数 終了